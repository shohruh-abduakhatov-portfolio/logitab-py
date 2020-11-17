import os  # NOQA: E402

import aiohttp_cors
import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_apispec import (
    setup_aiohttp_apispec,
    validation_middleware,
)


os.environ['CORE_CONFIG'] = '/var/www/config.py'  # NOQA: E402
print("config path: ", os.environ['CORE_CONFIG'])
# sys.path.append("../")
# print('>>>%s' % (sys.path))

from logi_web.db import init_pg, close_pg
from logi_web.settings import BASE_DIR, load_conf
from logi_web.urls import setup_routes, setup_routes_mobile
from logi_web.views.index import index


async def factory(debug=False):
    # Init
    app = web.Application()

    # load config
    app['config'] = load_conf(debug)

    # Routes
    app.router.add_get('/', index)
    setup_routes(app)
    setup_routes_mobile(app)

    # Cors Setup
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_headers="*",
            allow_credentials=True,
            expose_headers="*"
        )
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)

    # pg setup
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    # Ninja2 setup
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(BASE_DIR / 'templates')))

    # Swagger setup
    setup_aiohttp_apispec(
        app,
        swagger_path="/api/v1/doc",
        title='Logitab Documentaion',
        version='v1.1.0')

    # Register middleware
    app.middlewares.append(validation_middleware)

    return app


if __name__ == '__main__':
    web.run_app(factory(debug=True), port=8001)
