from random import randint
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp_jinja2 import template
from url_regex import UrlRegex
from . import db_interaction as db
from . utils import make_unique_link


@template("index.html")
async def index(request: Request):
    shorted_link = await make_unique_link(request)
    site_name = request.app["config"].get("site_name")
    return {"a": randint(1, 100),
            "b": randint(1, 100),
            "site_name": site_name,
            "shorted_link": shorted_link}


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

    url_regex = UrlRegex(data["url"])
    if url_regex.detect:
        print(url_regex.input)
        short_link = await make_unique_link(request)
        await db.insert_link(request, str(url_regex.input), short_link)
        return web.json_response({"url": short_link})
    else:
        return web.json_response({
                              "error": {
                                "code": 400,
                                "message": "Invalid URL"
                              }
                            }, status=400)


async def links(request: Request):
    result = await db.select_all(request)
    return web.Response(body=str(result))


async def api(request: Request):
    print(request.query)
    query = request.query
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
            await db.insert_link(request, str(url_regex.input), short_link)
            result["links"].append(short_link)
        else:
            result["links"].append(None)
    if any(result["links"]):
        result["code"] = 200
        result["message"] = f"You enter {i} links and {len(list(filter(bool, result['links'])))} of them is valid"
    return web.json_response({
            "code": result["code"],
            "message": result["message"],
            "links": result["links"]
    }, status=result["code"])
