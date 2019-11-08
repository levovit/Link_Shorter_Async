from random import randint
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp_jinja2 import template
from . import db_interaction as db
from . utils import make_link


@template("index.html")
async def index(request: Request):
    shorted_link= make_link(request.host)
    site_name = request.app["config"].get("site_name")
    return {"a": randint(1, 100),
            "b": randint(1, 100),
            "site_name": site_name,
            "shorted_link": shorted_link}


async def links(request: Request):
    result = await db.select_all(request)
    return web.Response(body=str(result))
