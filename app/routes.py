import pathlib
from aiohttp.web_app import Application
from app import views

BASE_DIR = pathlib.Path(__file__).parent.parent


def setup_routes(app: Application):
    app.router.add_get('/', views.index)
    app.router.add_get('/api', views.api)
    app.router.add_post('/short', views.short)
    app.router.add_static('/static/', path=BASE_DIR / "app" / "static", name="static")
    app.router.add_get('/{short_link}', views.redirect)
