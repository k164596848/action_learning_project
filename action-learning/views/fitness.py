
import os
from re import A
from aiohttp import web
from core.action import Action
from core.activity import Activity
from core.distribution import Distribution
from draw.video import Video
from util.openpose import save_to_json_path
from core.person import Person 
from core.base import *


# class FitnessView(web.View):
#     @property
#     def activity(self) -> Activity:
#         activity = self.request.match_info.get("activity", "")
#         try:
#             activity = Activity(activity)
#         except ValueError as identifier:
#             raise web.HTTPBadRequest(reason=identifier)
#         return activity

#     async def post(self):
#         """
#         ---
#         description: >
#           體適能測驗 {activity} 為所選擇的體適能項目  

#           可選擇的體適能項目為:
#             - 原地站立抬膝
#             - 椅子坐立
#             - 開眼單足立
#             - 椅子坐姿體前彎
#             - 肱二頭肌手臂屈舉
#         tags:
#         - Fitness
#         produces:
#         - application/json
#         requestBody:
#           content:
#             multipart/form-data:
#               schema:
#                 type: object
#                 properties:
#                   video:
#                     type: string
#                     format: binary
#                   gender:
#                     type: string
#                     default: "女"
#                   age:
#                     type: integer
#                     default: 65
#                   pointIndex:
#                     type: integer
#                     required: false
#         responses:
#             "200":
#                 description: finished!
#                 test
#         """
#         # XXX: flag: render skeleton?
#         # TODO: check gender and age
#         json_path = f"static/json/{self.request.uuid}/"
#         if Activity.SIT_FORWARD_ON_CHAIR: #sit_forward_on_chair(activity) need hands skeleton imformation, so we use "hand" augment to controll 
#             save_to_json_path(self.request.video, json_path, hand=True) 
#         else:
#             save_to_json_path(self.request.video, json_path)
                   
#         action = Action.from_json(json_path)
#         dist = Distribution(self.activity, gender=self.request.body["gender"], age=int(self.request.body["age"]))
#         action_level = action.evaluate(dist)#
#         video = Video(self.request.video)#the video from post() swagger api
#         video.draw_data(action.frames_data)
#         video.draw_info(action_level.get_info())
#         if "pointIndex" in self.request.body and self.request.body["pointIndex"].isnumeric():
#             point_idx = int(self.request.body["pointIndex"])
#             if 24 >= point_idx >= 0:
#                 video.draw_arcs(action.get_arcs(point_idx))
#         out_path = f"static/out/{self.request.uuid}.mp4"
#         video.export(out_path)
#         return web.json_response({"video": out_path, **action_level.get_info()})


class FitnessView(web.View):
    @property
    def activity(self) -> Activity:
        activity = self.request.match_info.get("activity", "")
        try:
            activity = Activity(activity)
        except ValueError as identifier:
            raise web.HTTPBadRequest(reason=identifier)
        return activity


    async def post(self):
       
        # XXX: flag: render skeleton?
        # TODO: check gender and age
        json_path = f"static/json/{self.request.uuid}/"

        #you can get the data from request thsahat you send

        #sit_forward_on_chair(activity) need hands skeleton imformation, so we use "hand" augment to controll 
        if Activity.SIT_FORWARD_ON_CHAIR: 
            save_to_json_path(self.request.video, json_path, hand=True) 
        else:
            save_to_json_path(self.request.video, json_path)

        #another classmethod using json file directly 
        person = Person.get_json_content(json_path,people_num=1)
        seperated_people  = separate_people(person,person.people_num)
        
        #two more peoeple and the 
        for i in range (0,person.people_num):
          #generate the Action object by directly using the json files 
          action = Action.from_list(seperated_people[i])
          
          #here will add the acion  recongniton function    
                
          #first people
          if(i == 0):
            dist = Distribution(self.activity, gender=self.request.body["gender"], age=int(self.request.body["age"]))
          #second people
          if(i == 1 ):
            # we can only use string to replace "activity、gender、age"
            dist = Distribution(self.activity, gender=self.request.body["gender"], age=int(self.request.body["age"]))

          print("people_num =",i)
          action_level = action.evaluate(dist)

          if(i==0):video = Video(self.request.video)#the videopath from post() swagger api requests
          #read the generated video again   
          if(i==1):video = Video(f"static/out/{self.request.uuid}{i-1}.mp4")
            
          #set the need to draw frame
          video.draw_data(action.frames_data)
          #set the tester information 
          video.draw_info(action_level.get_info())
          #check the pointIndex 
          if "pointIndex" in self.request.body and self.request.body["pointIndex"].isnumeric():
              #set the pointIdex variable
              print("pointIndex = ",self.request.body["pointIndex"])
              if(i ==1 ):point_idx = int(self.request.body["pointIndex"])
              if(i ==0 ):point_idx = int(self.request.body["pointIndex"])
              if 24 >= point_idx >= 0:
                if (point_idx==13 or point_idx ==10):
                    video.draw_arcs(action.get_arcs(13))
                    video.draw_second_arcs(action.get_arcs(10))
                else:
                    #set the arcs infomation
                    video.draw_arcs(action.get_arcs(point_idx))

          out_path = f"static/out/{self.request.uuid}{i}.mp4"
          #provide the info and count position
          position = list(action[30][0])
          video.export(out_path,position,num=(i+1))
            
        return web.json_response({"video": f"{self.request.uuid}{i}.mp4", **action_level.get_info()})
