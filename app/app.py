import pathlib

from aiohttp import web
from aiohttp.web_app import Application
import aiohttp_jinja2
import asyncpgsa
import jinja2

from .routes import setup_routes

BASE_DIR = pathlib.Path(__file__).parent.parent


async def create_app(config: dict, db_url: str = None) -> Application:
    app = web.Application()
    if db_url:
        config["database_uri"] = db_url
    app["config"] = config
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(BASE_DIR / 'app' / 'templates')))

    setup_routes(app)
    app.on_startup.append(on_start)
    app.on_cleanup.append(on_cleanup)
    return app


async def on_start(app):
    config = app["config"]
    app["db"] = await asyncpgsa.create_pool(dsn=config["database_uri"])


async def on_cleanup(app):
    await app["db"].close()
