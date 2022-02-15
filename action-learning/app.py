from os import makedirs

from aiohttp import web
from aiohttp_swagger import setup_swagger

from views import setup_routes
from web.middleware import store_video_middleware

#先進行新增資料夾
try:
    makedirs("static/video")
    makedirs("static/json")
    makedirs("static/out")
except FileExistsError:
    pass

async def make_app():
    
    app = web.Application(middlewares=[store_video_middleware])
    app.add_routes([web.static("/static", "static")])
    setup_routes(app)
    setup_swagger(app, swagger_url="/api/v1/doc", ui_version=3)
    return app


if __name__ == "__main__":
    web.run_app(make_app())
