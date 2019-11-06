from aiohttp_jinja2 import template
from random import randint


@template("index.html")
async def index(request):
    site_name = request.app["config"].get("site_name")
    return {"a": randint(1, 100),
            "b": randint(1, 100),
            "site_name": site_name}
