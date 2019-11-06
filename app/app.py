from aiohttp import web
import aiohttp_jinja2
import jinja2
import pathlib
from .routes import setup_routes

BASE_DIR = pathlib.Path(__file__).parent.parent


async def create_app(config: dict):
    app = web.Application()
    app["config"] = config
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(BASE_DIR / 'app' / 'templates')))

    setup_routes(app)
    return app
