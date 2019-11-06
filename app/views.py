from random import randint
from aiohttp import web
from aiohttp_jinja2 import template
from . import db_interaction as db


@template("index.html")
async def index(request):
    site_name = request.app["config"].get("site_name")
    return {"a": randint(1, 100),
            "b": randint(1, 100),
            "site_name": site_name}


async def links(request):
    result = await db.select_all(request)
    return web.Response(body=str(result))
