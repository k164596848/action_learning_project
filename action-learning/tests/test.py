import json
import sysconfig
import numpy as np
from pprint import PrettyPrinter
from core.action import Action
from core.base import Keypoints
from core.distribution import Distribution
from core.segmetation import segment
from core.part import Part
from draw import Video

import matplotlib.pyplot as plt
import asyncio
from util.base import separate_people
from core.person import Person


pp = PrettyPrinter(indent=4)
ppprint = pp.pprint

async def recongination_action(tester):

    keen = Action.from_json("tests/json/output_raiseleg/")[0:300]
    # keen = Action.from_json("tests/json/教練抬膝右/")[0:300]

    # left_hand =Action.from_json("tests/json/教練曲舉左/")[0:300]
    # right_hand = Action.from_json("tests/json/教練曲舉右/")[0:300]
    
    left_hand = Action.from_json("tests/json/測試曲舉左/")[0:300]
    right_hand = Action.from_json("tests/json/測試曲舉右/")[0:300]

    # sit_down  = Action.from_json("tests/json/教練坐立右/")[0:300]

    # fig = plt.figure()
    # plt.plot(tester.r_leg_ang,"-",label="tester")
    # plt.plot(keen.r_leg_ang,'-',label="compare_keen")
    # plt.plot(right_hand.r_leg_ang,"-",label="compare_right_hand")
    # plt.plot(left_hand.r_leg_ang,"-",label="compare_left_hand")
    # plt.legend()
    # plt.show()

    print("左手")
    compare_hand_L = tester.compare(left_hand,weighted=True,action="leftH")
    print("右手")
    compare_hand_R = tester.compare(right_hand,weighted=True,action="rightH")
    print("抬膝")
    compare_keen = tester.compare(keen,weighted=True,action="keen")
    
    # print("坐立")
    # compate_sit_down = tester.compare(sit_down)
    
    #選出相似值最大的那個，回傳動作
    target =list([compare_keen[Part.FULL_BODY],compare_hand_L[Part.FULL_BODY],compare_hand_R[Part.FULL_BODY]])
    # target =list([compare_keen[Part.FULL_BODY]])
    act = target.index(max(target))
    if (act == 0 ):return "原地站立抬膝"
    elif(act ==1 or act ==2):return "肱二頭肌手臂屈舉"
    elif(act ==3):return "椅子坐立"

    # print("抬膝")   
    # compare_keen = tester.compare(keen)
    # print("左手")
    # compare_hand_L = tester.compare(left_hand)
    # print("右手")
    # compare_hand_R = tester.compare(right_hand)


    # print(compare_keen)
    # print("\nhand_Left")
    # print(compare_hand_L)
    # print("hand_Right")
    # print(compare_hand_R)

    if(
        (compare_keen[Part.LEFT_LEG]>compare_hand_R[Part.LEFT_LEG] and compare_keen[Part.RIGHT_LEG]>compare_hand_R[Part.RIGHT_LEG]) 
        or 
        (compare_keen[Part.LEFT_LEG]>compare_hand_L[Part.LEFT_LEG] and compare_keen[Part.RIGHT_LEG]>compare_hand_L[Part.RIGHT_LEG])
        ):
        return "原地站立抬膝"
    else:
        return "肱二頭肌手臂屈舉"

    

def compare_videos():

    tester = Action.from_json("tests/json/leg_-3x/")[0:300]
    # tester = Action.from_json("tests/json/leg_3x/")[0:300]
    keen = Action.from_json("tests/json/output_raiseleg/")[0:300]
   

    # fig = plt.figure()
    # plt.plot(a1.r_leg_ang,"-",label="raise R_leg 8 times /10s")
    # plt.plot(a2.r_leg_ang,'-',label="raise R_leg 6 times /10s")
    # plt.legend()
    # plt.show()

    # a1 = Action.from_json("tests/json/教練曲舉右/")
    # a2 = Action.from_json("tests/json/教練抬膝右/")

    # a1 = Action.from_json("tests/json/dtw_dif_a1/")[0:300]
    # a2 = Action.from_json("tests/json/dtw_dif_a2/")[0:300]
    print("keen")
    tester.compare(keen,weighted=True,action ="keen")


def test_raise_leg():
    # counts is a list of frame index
    # action = Action.from_json("tests/json/output_raiseleg/")
    action = Action.from_json("tests/json/教練抬膝左/")
    dist = Distribution("原地站立抬膝", gender="男", age=80)
    action_level = action.evaluate(dist)
    print(action_level.get_info())
    

def test_raise_hand():
    # counts is a list of frame index
    action = Action.from_json("tests/json/教練曲舉左/")
    dist = Distribution("肱二頭肌手臂屈舉", gender="男", age=65)
    action_level = action.evaluate(dist)
    print(action_level.get_info())

def test_sit_down():
    # counts is a list of frame index
    action = Action.from_json("tests/json/output_1F/")
    dist = Distribution("椅子坐立", gender="女")
    action_level = action.evaluate(dist)


def test_stand_on_foot():
    action = Action.from_json("tests/json/output_5FR/")
    dist = Distribution("開眼單足立", gender="女")
    action_level = action.evaluate(dist)


def test_sitting_forward():
    action = Action.from_json("tests/json/阿北肢體前彎/")
    dist = Distribution("椅子坐姿體前彎", gender="女")
    action_level = action.evaluate(dist)


def test_body_direction():
    action = Action.from_json("tests/output_t-pose-rotate/")
    max = 0.0
    for idx, kps in enumerate(action):
        if idx == 0:
            max = kps.body_area
        print(idx + 1, kps.d(max))


def test_diff_capture():

    return None
    
def test_person():

    # video 72 的右手 openpose 有認定出錯的問題，
    # person = Person.get_json_content("tests/json/雙人抬舉72/",people_num=2)
    # person = Person.get_json_content("tests/json/雙人抬舉73/",people_num=2)
    # person = Person.get_json_content("tests/json/雙人抬舉74/",people_num=2)
    # person = Person.get_json_content("tests/json/雙人45度/",people_num=2)
    # person = Person.get_json_content("tests/json/雙人0度/",people_num=2)
    # person = Person.get_json_content("tests/json/三人不同77/",people_num=3)
    person = Person.get_json_content("tests/json/雙人n67/",people_num=2)

    # person = Person.get_json_content("tests/json/me正面/")
    # person = Person.get_json_content("tests/json/單人正面/")

    seperated_people  = separate_people(person,person.people_num)
   
    for i in range (0,person.people_num):
        action = Action.from_list(seperated_people[i])
        activity_name = asyncio.run(recongination_action(action[0:300]))
        dist = Distribution(activity_name, gender="男", age=65)
        action_level =action.evaluate(dist)
        # if(i ==0):dist = Distribution("原地站立抬膝", gender="男", age=70)
        # if(i ==1):dist = Distribution("肱二頭肌手臂屈舉", gender="男", age=80)
        
        position = list(action[30][0])
        position = (round(position[0]),round(position[1]))
        print("head position =",position)
        # print(action_level.get_info())

def test_capture_angle_limtation(json_folder):
    person = Person.get_json_content("tests/json/VID_20210616_"+str(json_folder) +"/")
    seperated_people  = separate_people(person,person.people_num)
   
    for i in range (0,person.people_num):
        action = Action.from_list(seperated_people[i])
        activity_name = asyncio.run(recongination_action(action[0:300]))
        dist = Distribution(activity_name, gender="男", age=65)
        action_level =action.evaluate(dist)
      
        position = list(action[30][0])
        position = (round(position[0]),round(position[1]))
        # print("head position =",position)
        # print(action_level.get_info())

    

if __name__ == "__main__":
    # test_person()
    
    # compare_videos()
    # recongination_action()
    # test_raise_leg()
    # test_raise_hand()
    # vid_list =["+0","+10","+20","+30","+40","+50","+60","+70","+80","+90","-10","-20","-30","-40","-50","-60","-70","-80","-90"]
    vid_list =["+0","+10","+20","+30","+40","+50","+60","+70","+80","+90"]
    for json_folder in vid_list:
        print("video_"+json_folder)
        test_capture_angle_limtation(json_folder)

  
