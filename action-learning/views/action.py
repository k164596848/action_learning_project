from aiohttp import web

from core.action import Action
from core.part import Part
from data import CoachData
from util.openpose import save_to_json_path


class ActionCoachView(web.View):
    async def get(self):
        return web.json_response({"coachs": CoachData.get()})

    async def post(self):
        """
        ---
        description: >
          input 教練影片及名稱
          return 教練影片id        
        tags:
        - Action
        produces:
        - application/json
        requestBody:
          content:
            multipart/form-data:
              schema:
                type: object
                properties:
                  video:
                    type: string
                    format: binary
                    default: "coach1.avi"
                  name:
                    type: string
                    default: "coach1"
        responses:
          "200":
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    video:
                      type: string
                      description: video path
                    uuid:
                      type: string
                    name:
                      type: string
        """
        if "name" not in self.request.body:
            raise web.HTTPBadRequest(reason="field 'name' not in body!")
        json_path = f"static/json/{self.request.uuid}/"
        save_to_json_path(self.request.video, json_path)
        # NOTE: to make sure there is one person in output json
        Action.from_json(json_path)
        ok = CoachData.add(
            {"uuid": self.request.uuid, "name": self.request.body["name"]}
        )
        if not ok:
            raise web.HTTPBadRequest(reason="uuid already exist!")
        return web.json_response(
            {
                "video": self.request.video,
                "uuid": self.request.uuid,
                "name": self.request.body["name"],
            }
        )


class ActionCompareView(web.View):
    async def post(self):
        """
        ---
        description: >
          上傳 受測者影片 並選擇與哪個教練（教練影片id）做動作比對        
        tags:
        - Action
        produces:
        - application/json
        requestBody:
          content:
            multipart/form-data:
              schema:
                type: object
                properties:
                  video:
                    type: string
                    format: binary
                  coach:
                    type: string
                    description: coach's uuid
        responses:
          "200":
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    result:
                      type: object
                      description: varying degrees of two human's each body part by using DTW
        """
        json_path = f"static/json/{self.request.uuid}/"
        coach_uuid = self.request.body["coach"]
        # 如果拿不到 coach 的 UUID 則 alter 
        if not coach_uuid in CoachData.get_uuids():
            raise web.HTTPBadRequest(
                reason=f"coach uuid '{coach_uuid}' does not exist!"
            )
        coach_path = f"static/json/{coach_uuid}/"
        save_to_json_path(self.request.video, json_path)
        action = Action.from_json(json_path)
        result = action.compare(Action.from_json(coach_path))
        return web.json_response({"result": Part.to_json_seriable_dict(result)})
