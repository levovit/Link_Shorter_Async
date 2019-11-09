from datetime import datetime, timedelta
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp_jinja2 import template
from url_regex import UrlRegex
from . import db_interaction as db
from . utils import make_unique_link


@template("index.html")
async def index(request: Request):
    site_name = request.app["config"].get("site_name")
    return {"site_name": site_name}


async def short(request: Request):
    data = await request.json()
    print(data)
    if "url" not in data:
        return web.json_response({
                              "error": {
                                "code": 415,
                                "message": "Data has no 'url' attribute"
                              }
                            }, status=415)
    days = 90
    if "days" in data:
        days = data["days"]
        if not days.isdecimal():
            return web.json_response({
                "error": {
                    "code": 400,
                    "message": "Invalid days number. Must be Integer"
                }
            }, status=400)
        else:
            days = int(days)
    if not (1 <= days <= 366):
        return web.json_response({
            "error": {
                "code": 400,
                "message": "Expiration date must be more than 1 day and less then year"
            }
        }, status=400)

    url_regex = UrlRegex(data["url"])
    if url_regex.detect:
        print(url_regex.input)
        short_link = await make_unique_link(request)
        await db.insert_link(request, str(url_regex.input), short_link, days, "web")
        return web.json_response({"url": short_link})
    else:
        return web.json_response({
                              "error": {
                                "code": 400,
                                "message": "Invalid URL"
                              }
                            }, status=400)


async def api(request: Request):
    print(request.query)
    query = {k: v for k, v in request.query.items()}

    days = query.pop("days", "90")
    if not days.isdecimal():
        return web.json_response({
            "error": {
                "code": 400,
                "message": "Invalid days number. Must be Integer"
            }
        }, status=400)
    else:
        days = int(days)
    active_until = datetime.utcnow() + timedelta(days)

    if not (1 <= days <= 366):
        return web.json_response({
            "error": {
                "code": 400,
                "message": "Expiration date must be more than 1 day and less then year"
            }
        }, status=400)

    if not query:
        return web.json_response({
            "error": {
                "code": 404,
                "message": "no links entered"
            }
        }, status=404)

    result = {"code": 400, "links": [], "message": "Invalid URL"}

    for i, key in enumerate(query):
        link = query[key]
        url_regex = UrlRegex(link)
        if url_regex.detect:
            print(url_regex.input)
            short_link = await make_unique_link(request)
            await db.insert_link(request, str(url_regex.input), short_link, days, "api")
            result["links"].append(short_link)
        else:
            result["links"].append(None)

    if any(result["links"]):
        result["code"] = 200
        result["message"] = f"You enter {i+1} links and {len(list(filter(bool, result['links'])))} of them is valid"

    return web.json_response({
            "code": result["code"],
            "message": result["message"],
            "links": result["links"],
            "active_until": str(active_until)
    }, status=result["code"])


@template("404.html")
async def redirect(request: Request):
    site_name = request.app["config"].get("site_name")
    short_link = request.host + "/" + request.match_info['short_link']

    query = await db.get_link(request, short_link)
    if not query:
        return {"site_name": site_name, "reason": f"Link - {short_link}  dont exist"}

    query = query[0]
    long_link = query[0]
    active_until = query[1]

    if datetime.utcnow() > active_until:
        return {"site_name": site_name, "reason": f"link - {short_link} expired"}

    return web.HTTPFound(location=long_link)
