
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
from core.recognition import *

class MultipleView(web.View):
    """
        ---
        description: >
          體適能測驗 {activity} 為所選擇的體適能項目  

          可選擇的體適能項目為:
            - 原地站立抬膝
            - 椅子坐立
            - 開眼單足立
            - 椅子坐姿體前彎
            - 肱二頭肌手臂屈舉
        tags:
        - Fitness
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
                  gender:
                    type: string
                    default: "女"
                  age:
                    type: integer
                    default: 65
                  pointIndex:
                    type: integer
                    required: false
                  person:
                    type: integer
                    default: 1
        responses:
            "200":
                description: finished!
                test
    """

  


    async def post(self):
       
        # XXX: flag: render skeleton?
        # TODO: check gender and age

        json_path = f"static/json/{self.request.uuid}/"

        #sit_forward_on_chair(activity) need hands skeleton imformation, so we use "hand" augment to controll 
     
        save_to_json_path(self.request.video, json_path)
        print(self.request.body.keys())
        #another classmethod using json file directly 
        person = Person.get_json_content(json_path,people_num=int(self.request.body["person"]))
        seperated_people  = separate_people(person,person.people_num)
        
        #multiple person generate and the
        for i in range (0,person.people_num):
          #generate the Action object by directly using the json files 
          action = Action.from_list(seperated_people[i])
          
          #here will add the acion  recongniton function    
          activity_name = recoginition(action[0:300])
          if(activity_name!="原地站立抬膝"):activity_name=activity_name[0:(len(activity_name)-1)]  
          #first people
          dist = Distribution(activity_name, gender=self.request.body["gender"], age=int(self.request.body["age"]))
          
          print("people_num =",i)
          action_level = action.evaluate(dist)

          if(i==0):video = Video(self.request.video)#the videopath from post() swagger api requests
          #read the generated video again   
          if(i!=0):video = Video(f"static/out/{self.request.uuid}{i-1}.mp4")
            
          #set the need to draw frame
          video.draw_data(action.frames_data)
          #set the tester information 
          video.draw_info(action_level.get_info())
          #check the pointIndex 
          # if "pointIndex" in self.request.body and self.request.body["pointIndex"].isnumeric():
              #set the pointIdex variable
          if(activity_name=="原地站立抬膝" ):point_idx = int(13)
          elif(activity_name=="肱二頭肌手臂屈舉" ):point_idx = int(6)#left_hand(6); right_hand(3)

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

        return web.json_response({"video": f"{self.request.uuid}{i}", **action_level.get_info()})
