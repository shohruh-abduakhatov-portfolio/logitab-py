import os

from aiohttp import web
from aiohttp_apispec import (
    docs
)


@docs(
    tags=["ping"],
    summary="ping server",
    description="Test connection",
)
async def test2(request):
    return web.json_response(
        "pong"
    )


async def update_app(request):
    print("/update_app")
    app = request.rel_url.query.get("app", "logitab-web-app")

    if app != "logitab-web-app":
        return

    import subprocess
    print("running script")
    p = os.path.abspath("/home/ubuntu/logi-back-py/scripts/update-project.sh")
    subprocess.Popen(["sh", p])

    return web.json_response(
        status=200,
        data="updated"
    )
