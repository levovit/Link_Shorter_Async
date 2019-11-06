import ssl
import pathlib
from aiohttp import web
import aiohttp_jinja2
import asyncpgsa
import jinja2

from .routes import setup_routes

BASE_DIR = pathlib.Path(__file__).parent.parent


async def create_app(config: dict):
    app = web.Application()
    app["config"] = config
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(BASE_DIR / 'app' / 'templates')))

    setup_routes(app)
    app.on_startup.append(on_start)
    app.on_cleanup.append(on_cleanup)
    return app


async def on_start(app):
    config = app["config"]
    ctx = ssl.create_default_context(cafile=BASE_DIR / "rds-ca-2019-eu-north-1.pem")
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    app["db"] = await asyncpgsa.create_pool(dsn=config["database_uri"], ssl=ctx)


async def on_cleanup(app):
    await app["db"].close()
