from __future__ import annotations

from math import cos, radians
import math
from statistics import mean
from typing import Dict, List, Set
import matplotlib.pyplot as plt
import numpy as np
from fastdtw import fastdtw
from dtw import *
from scipy import ndimage
from scipy.spatial.distance import euclidean

from core.activity import Activity
from core.base import Keypoints, Point
from core.distribution import Distribution
from core.part import Part
from data import ActionLevel
# from util.base import consecutive_one, distance2angle, get_angle, get_files_from_prefix
from util.base import *
import pprint



def fix_lost_skeletons(is_doings: List[bool], iterations=5):
    
    """Due to some skeletons will miss catch by openpose.
    We use binary_dilation and binary_erosion to 

    Args:
        is_doings (List[bool]): [description]
        iterations (int, optional): [description]. Defaults to 5.

    Returns:
        [type]: [description]
    """
    return ndimage.binary_erosion(
        ndimage.binary_dilation(is_doings, iterations=iterations),
        iterations=iterations,
        border_value=1,
    )


class Action(List[Keypoints]):

    #action like=> 抬膝、曲舉、坐立
    _counts:int

    fps: float = 30

    activities: Dict[Activity, dict] = {
        Activity.SIT_DOWN_AND_STAND_UP: {"seconds": 30},
        Activity.RAISE_KNEE_IN_PLACE: {"seconds": 120},
        Activity.RAISE_HANDS:{"seconds":30}, 
        Activity.EYES_OPEN_STAND_ON_FOOT: {"seconds": 30},
        Activity.SIT_FORWARD_ON_CHAIR: {"seconds": 30},
    }
    
    # NOTE: parts 角度索引
    parts: Dict[Part, Set] = {
        Part.LEFT_SHOULDER: {5},
        Part.RIGHT_SHOULDER: {4},
        Part.LEFT_ARM: {7},
        Part.RIGHT_ARM: {6},
        Part.LEFT_LEG: {13},
        Part.RIGHT_LEG: {12},
       
    }
    # parts: Dict[Part, Set] = {
    #     Part.LEFT_SHOULDER: {2, 4},
    #     Part.RIGHT_SHOULDER: {3, 5},
    #     Part.LEFT_ARM: {4, 6},
    #     Part.RIGHT_ARM: {5, 7},
    #     Part.LEFT_LEG: {11, 13},
    #     Part.RIGHT_LEG: {10, 12},
    # }
    
    #store the number(index) of frames which have counts
    frames_data: list = []
  
    def __init__(self,*args, **kwargs):#初始化
        self.is_doing_activity = None
        super().__init__(*args, **kwargs)
                
    def __getitem__(self, index) -> Action:
        """this function can let you use action[0]....action[1] call classmethod or property """
        return Action(super().__getitem__(index))

    @classmethod#main program started 
    def from_json(cls, prefix: str, **kwargs) -> Action:
        """here is the Action's object newing, using classmethod(cls),which can call or use almost all methods in the Keypoints class 

        Arguments:prefix(srt):the json path.

        Return: cls function 
        """
       
        return cls(
            # get_files_from_prefix:read the json's file name in folder,save json_path as list[] datatype
            # Keypoints.from_json():the keypoits list[] turn to keypoint's Class 
            list(map(Keypoints.from_json, get_files_from_prefix(prefix, **kwargs)))
        )

    @classmethod#main program started 
    def from_list(cls, seperated_person: list) -> Action:
        """This is for the multiple person calss generate, here is the Action's object newing, using classmethod(cls), 
        which can call or use almost all methods in the Keypoints class 
        """
        return cls(
            list(map(Keypoints.from_list, seperated_person))
        )

    @property
    def angles(self) -> List[List[float]]:
        """action.angles property"""
        
        return [kps.angles for kps in self]
    @property
    def r_leg_ang(self) -> List[List[float]]:
        """ r_leg_ang action.angles property"""
        return [kps.angles[13] for kps in self]

    @property
    def l_leg_ang(self) -> List[List[float]]:
        """ r_leg_ang action.angles property"""
        return [kps.angles[12] for kps in self]

    def get_arcs(self, point_idx: int) -> List[List[Point]]:
        """Get arcs points list
        Args:
            point_idx (int): Specific point index ref to Body25
        Returns:
            List[List[Point]]: List of list of 3 points ref to `Keypoints.get_arc`
        """
        return [kps.get_arc(point_idx) for kps in self]

    # @property
    def weights(self, **kwargs) -> Dict[Part, float]:
        """[WIP] Calcualte weights for every `Part` by core keypoint distance.

        Returns:
            Dict[Part, float] -- Corresponding weight of part
        """
        # raise NotImplementedError("有點怪怪的 {m} 會抓錯 可能要加入 confidence 或 3D")
        weights = {}
        #24 angles in each frame,Format: frame1[ang0,ang1...ang24]
        angles_seq = np.array([kps.angles for kps in self]).T
        #計算each frame 角度變異數，以軸1為計算範圍，取最大值(which means activatic joint)
        m = np.argmax(angles_seq.var(axis=1))

        ang_var =list(angles_seq.var(axis=1))
        
        #coach的keypoints序列 ,length =25
        kps_seq = np.transpose(np.array(self), (1, 0, 2))
        # 全為 m 關節的位置矩陣; m_matrix length = 25

        #挑出關鍵(最大變異數)angle,複製300frames
        m_matrix = np.tile(kps_seq[Part.to_body25(m)], (len(kps_seq), 1, 1))
        
        # 距離 x, y 差矩陣
        dist_matrix = kps_seq - m_matrix
        # sqrt( x^2 + y^2 )
        dist_matrix = np.sqrt((dist_matrix ** 2).sum(axis=2))
        # 平均距離
        dists = np.mean(dist_matrix, axis=1)
        # Aggregate to part
        for key, idxs, in self.parts.items():
            #here idxs have more than one joint so using the list comprehansion to solve it 
            weights[key] = dists.max() - mean(
                map(lambda idx: dists[Part.to_body25(idx)], idxs)
            )
        weigts_sum = sum(weights.values())
        for key, value in weights.items():
            weights[key] = value / weigts_sum
        # assert sum(weights.values()) == 1

        #自動試算權重[weighted = auto]
        # mean_ang = mean(weights.values())
        # std_ang = np.std(np.array(list(weights.values())),ddof=0)
        # weigts_sum = sum(list(map(lambda x: 1 if x>mean_ang else 0 ,weights.values()))) 

        

        if(kwargs["weight"]): w_list=kwargs["weight"]
        #04/12 rewrite weights
        flag =-1 
        for key, idxs, in self.parts.items():
            #人為介入，將 權重 輸入進去4/22
            flag=flag+1
            weights[key] = w_list[flag]

        weights_sum = sum(weights.values())

        for key, value in weights.items():
            weights[key] = value / weights_sum
                
        # print("the weight ==>",weights)
        return weights

    def compare( self, other: Action, dist=euclidean, weighted=False, **kwargs) -> Dict[Part, float]:
        """Compare to another {Action} perhaps {other} is coach when {weighted} is {True}
        Arguments:
            other {Action} -- Another action
        Keyword Arguments:
            dist {Callable} -- Distance algorithmn (default: {euclidean})
            weighted {bool} -- [description] (default: {True})      
        Returns:
            Dict[Part, float] -- Similarity of between self and another actions
        """
        # print(list(self.parts

        
        results = {}
        for key, angles in self.parts.items():
            sim_of_part = []

            for angle in angles:
            
                #kps = Action object or Keypoints object
                tester_angles = [kps.angles[angle] for kps in self]
                target_angles = [kps.angles[angle] for kps in other]

                # if (kwargs["action"]=="keen" and (angle ==13 or angle==12)):print((np.mean(tester_angles)))
                if(angle ==13 or angle==12):
                    joint_lower_bound = 45
                elif(angle==6 or angle ==7):
                    joint_lower_bound = 35
                else:
                    joint_lower_bound = (np.mean(tester_angles))
                    
            

                #將tester angles 做平均，計算出lower bound
                # low_bound_angles  = np.ones(300,np.uint0)*(np.mean(tester_angles))0
                low_bound_angles  = np.ones(300,np.uint0)*joint_lower_bound
                low_bound,low_path =fastdtw(low_bound_angles, target_angles, dist=dist)

                #caculate the DTW distance 
                distance, path = fastdtw(tester_angles, target_angles, dist=dist)

                # if((angle==6 and kwargs["action"]=="rightH" )):
                #     # print(angle,"右12;左13")
                #     alignment = dtw(tester_angles, target_angles, keep_internals=True)
                #     alignment.plot(type="threeway")
                #     # dtw(tester_angles, target_angles, keep_internals=True, 
                #     # step_pattern=rabinerJuangStepPattern(6, "c")).plot(type="twoway",offset=-2)

                #keen => 50~180 degree
                #elbow => 35~180 degree 
                #hip => 50 ~180 degree
                
                                             
                distance = distance / min(len(tester_angles), len(target_angles))
                #根據normalize 0是最相似，cos(0) = 1 , cos(1) = 0
                #平均每一幀的distance

                
                
                # beta = 1-((low_bound/300)/180)
                beta = cos(radians(low_bound/300))
                beta = (beta+1)/2

                # sim_of_angle = cos(radians(distance))
                # sim_of_angle = 1-(distance/180)

                sim_of_angle = cos(radians(distance))
                sim_of_angle = (sim_of_angle+1)/2

                sim_of_angle = (sim_of_angle -beta) /(1-beta)

                #做sigmod function 調整
                # sigmoid = lambda x: 1 / (1 + math.exp(-12*x+7.5))
                # sim_of_angle=sigmoid(sim_of_angle)
                
                # NOTE: similarity >= 70% 則視為完全正確 基於 徐明睿（2019）的論文
                # Ref: https://hdl.handle.net/11296/5v97c3
                # if sim_of_angle >= 0.7:
                #     sim_of_angle = 1

                sim_of_part.append(sim_of_angle)
            
            #之前會有兩個角度合成一個part(部位)的 similarity,所以使用 mean()，目前是single joint
            results[key] = mean(sim_of_part)

        # Calculate full body similarity
        if weighted:
            weights = other.weights(weight =kwargs["weight"])
            results[Part.FULL_BODY] = sum(results[k] * weights[k] for k in self.parts)
        else:
            results[Part.FULL_BODY] = mean(results.values())
        # print(results,"some body_parts")
        print(results[Part.FULL_BODY],"fullbody")
        return results

    def evaluate(self, target: Distribution) -> ActionLevel:
        """Evaualte current action on specific distribution 
        Arguments:
            target {Distribution} -- target distribution
        Returns:
            ActionLevel -- Details of user's level
        """
       
        self.activity = target.activity
        if target.activity == Activity.SIT_FORWARD_ON_CHAIR:#椅子肢體前彎
            reverse = True
            self.is_doing_activity = None
            self.frames_data = self.distances(target.height)
            data = min(self.frames_data)
        else:
            reverse = False
            self.is_doing_activity = getattr(#只是單純抓activty名稱
                self, f"is_doing_{target.activity.name.lower()}"
            )
            if target.activity == Activity.EYES_OPEN_STAND_ON_FOOT:#開眼單足立
                self.frames_data = self.to_frames(self.durations())
                data = self.duration()
            elif target.activity == Activity.RAISE_KNEE_IN_PLACE:#原地站立抬膝
                self._counts = self.counts_RAISE_KNEE()
                self.frames_data = self.to_frames(self._counts)
                data = self.frequency(self._counts)
            elif target.activity == Activity.RAISE_HANDS:#肱二頭肌屈舉
                self._counts= self.counts_RAISE_HAND()
                self.frames_data = self.to_frames(self._counts)
                data = self.frequency(self._counts)
            else:#椅子坐立
                self.frames_data = self.to_frames(self.counts())
                data = self.frequency()
                
        print(target.activity.value, target.gender, target.age, data, reverse,"| from action calss evaluate()")
        return ActionLevel(
            target.activity.value, target.gender,target.age, data=data, reverse=reverse,
        )

    @staticmethod
    def to_frames(data: List[float]) -> List[float]:
        """Convert data (durations / counts) to frames for video drawing"""
        if not data:
            return []
        cbt = []
        counter = 0
        for times in range(data[-1] + 1):
            if times in data:
                counter += 1
            cbt.append(counter)
        return cbt

    def counts(self)->List[int]:
        
        is_doings = fix_lost_skeletons(list(map(self.is_doing_activity, self)))
        _counts = []
        for index, is_doing in enumerate(is_doings):
            if index == 0:
                continue
            if is_doing and not is_doings[index - 1]: # 
                _counts.append(index)

        return _counts

    def counts_RAISE_KNEE(self) -> List[int]:
        """Get all counts from frames while activity is happening

        Returns:
            List[int] -- frames index
        """
        # is_doings -> [True, True, False, True, ...]
        # True: doing, False: not doing
        
        
        left_thigh_list  = list(map(get_left_thigh,self))
        right_thigh_list = list(map(get_right_thigh,self))
        
        
        
        #try to write running average in a new way 
        #use the right thigh max list convert to a reliable right thigh max list 
        reliable_left_list = convert_reliable_thighMax_list(30,left_thigh_list)
        reliable_right_list = convert_reliable_thighMax_list(30,right_thigh_list)
        
        #angle_list 會回傳有角度angle值的list
        # angle_list = list(map(self.is_doing_return_angle, self))
        left_leg_list = list(map(self.left_angle_list,self,reliable_left_list))
        right_leg_list = list(map(self.right_angle_list,self,reliable_right_list))
        # left_leg_list_p2a = list(map(self.left_angle_list_p2a,self))
        # right_leg_list_p2a = list(map(self.right_angle_list_p2a,self))
     
        start =600
        end =900

        # fig = plt.figure()
        # plt.plot(right_thigh_list,"-", reliable_right_list,'-',right_leg_list,'-',np.linspace(110,110,len(right_leg_list)),'-',np.linspace(150,150,len(right_leg_list)),'-')
        # plt.plot(left_thigh_list,"-", reliable_left_list,'-',left_leg_list,'-',np.linspace(110,110,len(left_leg_list)),'-',np.linspace(150,150,len(left_leg_list)),'-')
        # # plt.plot(left_leg_list_p2a[0:300],'-',left_leg_list[0:300],'--',left_thigh_list[0:300],"-",np.linspace(110,110,len(left_leg_list[0:300])),'-',np.linspace(150,150,len(left_leg_list[0:300])),'-')
        # plt.plot(right_leg_list_p2a[start:end],'-',right_leg_list[start:end],'--',right_thigh_list[start:end],"-",np.linspace(110,110,len(left_leg_list[start:end])),'-',np.linspace(150,150,len(left_leg_list[start:end])),'-')
        # plt.xlabel("frames")
        # plt.ylabel("Angle& the thigh Max ")
        # plt.title('thigh and angle')
        # plt.show()

        _counts = []
        
        #left leg count
        _conut_left=[] 
        left_flag = 0
        for i in range(0,len(left_leg_list)):
            if (left_flag == 0):#放下的狀態
                if(left_leg_list[i]<110):#這裡的threashold 要在另寫function
                    left_flag=1           
                    _counts.append(i)
                    _conut_left.append(i)
            else:#flag=1,抬起的狀態
                if(left_leg_list[i]>150):left_flag = 0
                    
        #right leg count
        _conut_right=[] 
        right_flag = 0
        for j in range(0,len(right_leg_list)):
            if (right_flag == 0):#放下的狀態
                if(right_leg_list[j]<110):#這裡的threashold 要在另寫function
                    right_flag=1           
                    _counts.append(j)
                    _conut_right.append(j)
            else:#flag=1,抬起的狀態
                if(right_leg_list[j]>150):
                    right_flag = 0
                    
                                      
        # print(right_leg_list)
        _counts=sorted(_counts)

        print("conut_left",len(_conut_left))
        print("conut_right",len(_conut_right))
        

        print("_counts",_counts) 
        print("_counts_num",len(_counts))
        return _counts

    def counts_RAISE_HAND(self)->List[int]:
        _counts = []
        # is_doings = fix_lost_skeletons(list(map(self.is_doing_activity, self)))
        
        # for index, is_doing in enumerate(is_doings):
        #     if index == 0:
        #         continue
        #     if is_doing and not is_doings[index - 1]: # 
        #         _counts.append(index)

        # is_doing_ang = list(map(self.return_p2a_angle,self))

        left_hand_ang_list = list(map(self.left_hand_ang,self))
        right_hand_ang_list = list(map(self.right_hand_ang,self))

        #left hand count
        _conut_left=[] 
        left_flag = 0
        for i in range(0,len(left_hand_ang_list)):
            if (left_flag == 0):#放下的狀態
                if(left_hand_ang_list[i]<40):#這裡的threashold 要在另寫function
                    left_flag=1
                    _conut_left.append(i)
            else:#flag=1,抬起的狀態
                if(left_hand_ang_list[i]>145):
                    left_flag = 0
                    
        #right hand count
        _conut_right=[]
        right_flag = 0
        for j in range(0,len(right_hand_ang_list)):
            if (right_flag == 0):#放下的狀態
                if(right_hand_ang_list[j]<40):#這裡的threashold 要在另寫function
                    right_flag=1           
                    _conut_right.append(j)
            else:#flag=1,抬起的狀態
                if(right_hand_ang_list[j]>145):
                    right_flag = 0

        #哪一隻手的次數最多選就選那隻手
        if(len(_conut_left)>len(_conut_right)):
            _counts = _conut_left
        else:
            _counts = _conut_right

        _counts=sorted(_counts)
        
        print("conut_left",len(_conut_left))
        print("conut_right",len(_conut_right))
        
        print("_counts",_counts) 
        print("_counts_num",len(_counts))

        return _counts

    def counts_ang(self,angle_list,true_positive,true_negative) -> list[int] :#deactivate function
        """ 
        try to using angle to calculus the true negative and true positive action 
        應該要用 angle 轉 True and False
        Return: List[int]-- frames index 

        Arg :is_doing->[ang,ang,ang,..., ang]

        """ 
        _counts = []
        flag = 0
        for i in range(0,len(angle_list)):
            if (flag == 0):#放下的狀態
                if(angle_list[i]<true_positive):#這裡的threashold 要在另寫function
                    flag=1
                    print("look flag1 deail =",i,angle_list[i-1],angle_list[i],angle_list[i+1])
                    _counts.append(i)
            else:#flag=1,抬起的狀態
                if(angle_list[i]>true_negative):
                    flag = 0                   
        print("_counts:form counts_ang()",_counts)
        return               

    def count(self) -> int:
        """Count of activity happening

        Returns:
            int -- count
        """
        return len(self.counts)

    @staticmethod
    def is_doing_sit_down_and_stand_up(keypoints: Keypoints, threashold=150) -> bool:
        """To check is doing "椅子坐立" or not. 椅子坐立：受測者站立起身然後坐下來成原來姿勢。
        First, calculate vertical points of left and right knees keypoints -> vertical_points
        then use vertical_points, knees keypoints and thigh points to get included angle.
        Use the angle is less than threashold or not to determine sitting or standing.
        
        Args:
            keypoints (Keypoints) -- https://drive.google.com/file/d/1JPoAzpX74uv0zMgTMUtrrO9GG6Epk6YM/view?usp=sharing
            threashold (int, optional) -- Defaults to 150.

        Returns:
            bool -- return is doing or not (True or False)
        """
        vertical_points = [
            (keypoints[10].x, keypoints[10].y +1),
            (keypoints[13].x, keypoints[13].y +1),
        ]
        return (
            get_angle(vertical_points[0], keypoints[10], keypoints[9]) <= threashold
            or get_angle(vertical_points[1], keypoints[13], keypoints[12]) <= threashold
        )

    @staticmethod
    def is_doing_raise_knee_in_place(keypoints: Keypoints, threashold=110) -> bool:
        """To check is doing "原地站立抬膝" or not. 原地站立抬膝：做原地踏步動作，每一步踏步前膝蓋都必須抬到標示的高度。
        First, calculate vertical points of left and right thigh keypoints -> vertical_points
        then use vertical_points, thigh keypoints and knees points to get included angle.
        Use the angle is less than threashold to determine the foot lifted up.

        Args:
            keypoints (Keypoints) -- https://drive.google.com/file/d/1JPoAzpX74uv0zMgTMUtrrO9GG6Epk6YM/view?usp=sharing
            threashold (int, optional) -- Defaults to 110.

        Returns:
            bool -- return is doing or not (True or False)
        """
        
        vertical_points = [
            (keypoints[9].x, keypoints[9].y - 100),
            (keypoints[12].x, keypoints[12].y - 100)
            ]
        
       
        value = (get_angle(vertical_points[0], keypoints[9], keypoints[10]) <= threashold
        or get_angle(vertical_points[1], keypoints[12], keypoints[13]) <= threashold)
      
        return (
            value
            # get_angle(vertical_points[0], keypoints[9], keypoints[10]) <= threashold
            # or get_angle(vertical_points[1], keypoints[12], keypoints[13]) <= threashold

            # distance2angle(vertical_points[0], keypoints[9], keypoints[10]) <= threashold
            # or distance2angle(vertical_points[1], keypoints[12], keypoints[13]) <= threashold

            # (get_angle(vertical_points[0], keypoints[9], keypoints[10]) <= threashold or distance2angle(vertical_points[0], keypoints[9], keypoints[10]) <= threashold)
            # or
            # (get_angle(vertical_points[1], keypoints[12], keypoints[13]) <= threashold or distance2angle(vertical_points[1], keypoints[12], keypoints[13]) <= threashold)
        )

    @staticmethod
    def return_p2a_angle(keypoints: Keypoints) ->float:#not using fuction 

        vertical_points = [
            (keypoints[3].x, keypoints[3].y - 100),
            (keypoints[6].x, keypoints[6].y - 100),
        ]
        
        p2a_right = get_angle(vertical_points[0], keypoints[3], keypoints[4])
        p2a_left = get_angle(vertical_points[1], keypoints[6], keypoints[7])

        hand=(int(p2a_left),int(p2a_right))
       
        return hand

    @staticmethod 
    def right_hand_ang(keypoints:Keypoints)->float:
        vertical_points = [
           (keypoints[3].x, keypoints[3].y - 100)
        ]
        p2a_right = get_angle(vertical_points[0], keypoints[3], keypoints[4])
        return p2a_right

    @staticmethod 
    def left_hand_ang(keypoints:Keypoints)->float:
        vertical_points = [
            (keypoints[6].x, keypoints[6].y - 100)
        ]
        p2a_left = get_angle(vertical_points[0], keypoints[6], keypoints[7])
        return p2a_left
       
    @staticmethod
    def right_angle_list(keypoints: Keypoints,runningMax) ->float:
        """"""

        vertical_points = [
            (keypoints[9].x, keypoints[9].y - 100),
        ]

        p2a_right = get_angle(vertical_points[0], keypoints[9], keypoints[10])

        d2a_right = distance2angle(vertical_points[0], keypoints[9], keypoints[10],thighMax=runningMax)
            
        final_angle=0

        min_p2a=p2a_right
        min_d2a=d2a_right

        if(min_p2a<=120):#優先權 p2a>d2a
            min_final=min_p2a
        else:
            min_final = min(min_p2a,min_d2a)        
        
        final_angle=min_final
        return int(d2a_right)

    @staticmethod
    def left_angle_list(keypoints: Keypoints,runningMax) ->float:

       
        vertical_points = [
            (keypoints[12].x, keypoints[12].y - 100),
        ]
        p2a_left = get_angle(vertical_points[0], keypoints[12], keypoints[13])

        d2a_left = distance2angle(vertical_points[0], keypoints[12], keypoints[13],thighMax=runningMax)

        final_angle=0

        min_p2a=p2a_left
        min_d2a=d2a_left

        if(min_p2a<=120):#優先權 p2a>d2a
            min_final=min_p2a
        else:
            min_final = min(min_p2a,min_d2a)        
        
        final_angle=min_final 
        
        return int(d2a_left)

    @staticmethod
    def left_angle_list_p2a(keypoints: Keypoints) ->float:

        vertical_points = [
            (keypoints[12].x, keypoints[12].y - 100),
        ]
        p2a_left = get_angle(vertical_points[0], keypoints[12], keypoints[13])

        return int(p2a_left)
    
    @staticmethod    
    def right_angle_list_p2a(keypoints: Keypoints) ->float:

        vertical_points = [
            (keypoints[9].x, keypoints[9].y - 100),
        ]

        p2a_right = get_angle(vertical_points[0], keypoints[9], keypoints[10])

        return int(p2a_right)  
    
    @staticmethod
    def is_doing_raise_hands(keypoints: Keypoints, threashold=70) -> bool:
        """肱二頭肌屈舉計算
        """
        vertical_points = [
            (keypoints[3].x, keypoints[3].y - 30),#固定右手
            (keypoints[6].x, keypoints[6].y - 30),#固定左手
        ]

        return (
            get_angle(vertical_points[0], keypoints[3], keypoints[4]) <= threashold
            or get_angle(vertical_points[1], keypoints[6], keypoints[7]) <= threashold
        )

    @staticmethod
    def is_doing_eyes_open_stand_on_foot(keypoints: Keypoints, threashold=10) -> bool:
        """To check is doing "開眼單足立" or not. 開眼單足立：受測者雙手叉腰，以慣用腳站立並將另一隻腳置於支撐腳踝內側。
        Assuming that the initial action is standing on both feet.
        Once the knee is higher than the other one above the threashold, it means doing.

        Args:
            keypoints (Keypoints) -- https://drive.google.com/file/d/1JPoAzpX74uv0zMgTMUtrrO9GG6Epk6YM/view?usp=sharing
            threashold (int, optional) -- Defaults to 10.

        Returns:
            bool -- return is doing or not (True or False)
        """
        # TODO: 要切分成左腳跟右腳
        return abs(keypoints[10].y - keypoints[13].y) >= threashold

    @staticmethod
    def sit_forward_on_chair(keypoints: Keypoints, height: float) -> float:
        """To calculate the hand and feet euclidean distance in real life. 
        椅子坐姿體前彎：雙手上下重疊中止尖齊平並緩慢向前彎並計算中指指尖與腳尖的距離，若手指超過腳尖，以正分紀錄，反之則以負分紀錄。
        Calculate the tip of hand Keypoints and tip of feet Keypoints distance, 
        and use the person height to convert distance in the video to distance in the real life.

        Args:
            keypoints (Keypoints) -- https://drive.google.com/file/d/1JPoAzpX74uv0zMgTMUtrrO9GG6Epk6YM/view?usp=sharing
            height (float) -- Person's real height
        keypoints:
            keypoints[22]:右腳尖    
            keypoints[19]:左腳尖
            hand_right[12]:右手中指
            hand_left[12]:左手中指    

        Returns:
            float -- The hand and feet euclidean distance in real life
        """
        ratio = height / keypoints.height
        hands = [keypoints.hand_right[12], keypoints.hand_left[12]]
        feet = [keypoints[19], keypoints[22]]
        dist = ratio * min(
            sum(
                [
                    [
                        euclidean(hand, foot)
                        if hand[1] <= foot[1]
                        else -euclidean(hand, foot)
                        for foot in feet
                    ]
                    for hand in hands
                ],
                [],
            )
        )

        # print(keypoints.hand_left[9],keypoints.hand_left[12],keypoints[19])
        
      

        return dist

    def distances(self, height=177) -> List[float]:
        """Get all distances by using person height and body25 keypoints. 

        Args:
            height (int, optional): Person height. Defaults to 165.

        Returns:
            List[float]: distances for every frames
        """
        
        distance_for_each_frames = [self.sit_forward_on_chair(keypoints, height) for keypoints in self]
        # print(distance_for_each_frames)
        fig = plt.figure()
        plt.plot(distance_for_each_frames,"-")
        plt.xlabel("frames")
        plt.ylabel("cm ")
        plt.title('distance')
        # plt.show()
        return distance_for_each_frames

    def frequency(self,_counts=[], seconds=-1) -> float:
        """Activity frequency per second

        Keyword Arguments:
            seconds {int} -- Consider seconds (default: {-1})

        Returns:
            float -- frequency per second
        """
        # _counts = self.counts()
        if not _counts:
            return 0
        #have the fist action count frames
        first_frame = _counts[0]
        #get the specific activity's seconds
        if not seconds >= 0:
            seconds = self.activities[self.activity]["seconds"]
        
        #如果被count的frame(list) < (合理時間範圍)[第一個被count的frame+動作時長*fps(30)],才可通過filter
        # frequency = len(list( filter(lambda frame: frame < first_frame + seconds * self.fps, _counts ))) / seconds
        
        if(int(len(self)/self.fps)<seconds):
            frequency = len(list( filter(lambda frame: frame < first_frame + seconds * self.fps, _counts ))) / int(len(self)/self.fps)
            
        else:
            frequency = len(list( filter(lambda frame: frame < first_frame + seconds * self.fps, _counts )))  / seconds

        return frequency * seconds
            

    def durations(self) -> List[float]:
        """Get longest durations to **current frame**
        by using longest consecutive `True` (is doing action).
        This method is 'only' for drawing video!!!

        Returns:
            List[float]
        """
        previous_longest = 0
        _durations = []
        for index, keypoints in enumerate(self):
            longest = (
                consecutive_one(map(self.is_doing_activity, self[: index + 1]))
                // self.fps
            )
            if longest > previous_longest:
                _durations.append(index)
            previous_longest = longest
        return _durations

    def duration(self) -> float:
        """Get duration, by using longest consecutive `True` (is doing action) 

        Returns:
            float: 持續時間: 動作發生的時間點以秒為單位
        """
        is_doings = list(map(self.is_doing_activity, self))
        return consecutive_one(is_doings) / self.fps
 