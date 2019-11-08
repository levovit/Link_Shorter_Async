from random import randint
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp_jinja2 import template
from url_regex import UrlRegex
from . import db_interaction as db
from . utils import make_link


@template("index.html")
async def index(request: Request):
    shorted_link = make_link(request.host)
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
        shorted_link = make_link(request.host)
        return web.json_response({"url": shorted_link})
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
