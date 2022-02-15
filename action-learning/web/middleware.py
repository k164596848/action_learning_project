import os
from uuid import uuid4
from aiohttp import web
from aiohttp.web import middleware

#中介處理 http request 可以在新增或修改一些東西進去
@middleware
async def store_video_middleware(request, handler):
    if (request.method == "POST" and request.has_body):
        reader = await request.multipart()
        # print(vars(request).keys())
        #         
        request.body = {}
        async for field in reader:
            if field.name == "video":#處理video 
                uuid = str(uuid4())
                video_path = os.path.join(
                    "static/video/", uuid + "." + field.filename.split(".")[-1]
                )
                # TODO: check content is video
                with open(video_path, "wb") as f:
                    while True:
                        chunk = await field.read_chunk()
                        if not chunk:
                            break
                        f.write(chunk) # 寫入video
                request.video = video_path
                request.uuid = uuid
            else:#處理其他東西
                request.body[field.name] = await field.text()
        print(request.body.keys())
        if not getattr(request, "video", None):
            raise web.HTTPBadRequest(reason="Video field not found")

    return await handler(request)
