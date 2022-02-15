from __future__ import annotations

import math
from json import load
from typing import Dict, List, Union
import numpy as np
from scipy.spatial.distance import euclidean
import pprint

# from util.base import body25_to_angle24, get_graph, polygon_area
from util.base import *


class EmptyPeopleError(Exception):
    pass


class Point(tuple):
    """json files turned Piont class and caculate"""
    person_id :int
    x: float #video width
    y: float #video height
    confidence: float 

    def __new__(cls, x, y, confidence: float,person_id =0):
        return super().__new__(cls,(x, y))#繼承tuple??

    def __init__(self, x, y, confidence: float,person_id=0):
        self.confidence = confidence
    
    def __add__(self, other: Union[Point, float, int]) -> Point:
        if isinstance(other, Point):
            return Point(
                self.x + other.x,
                self.y + other.y,
                (self.confidence + other.confidence) / 2,
            )
        elif isinstance(other, float) or isinstance(other, int):
            return Point(self.x + other, self.y + other, self.confidence)
        else:
            raise NotImplementedError(type(other))

    def __sub__(self, other: Union[Point, float, int]) -> Point:
        if isinstance(other, Point):
            return Point(
                self.x - other.x,
                self.y - other.y,
                (self.confidence + other.confidence) / 2,
            )
        elif isinstance(other, float) or isinstance(other, int):
            return Point(self.x - other, self.y - other, self.confidence)
        else:
            raise NotImplementedError(type(other))
   

    @property#when call 'Point.x'  will return self[0]==x
    def x(self) -> float:
        return self[0]

    @property
    def y(self) -> float:
        return self[1]

    @classmethod
    def from_sequence(cls, sequence: list[float]) -> List[Point]:
        """
        """
        return [
            #sequence[i]:x coordinate, sequence[i+1]:y coordinate ,sequence[i+2]:confidence
            cls(sequence[i], sequence[i + 1], sequence[i + 2])
            for i in range(0, len(sequence), 3)
        ]

    @classmethod #you can delete 
    def person_sequence(cls, sequence:list[float]):
         
        return [
            cls(person_id = sequence[i])
            for i in range(0,len(sequence))
        ]
        


class Vector(list):
    def dot(self, vector) -> float:
        return sum((a * b) for a, b in zip(self, vector))

    def det(self, vector) -> float:
        """determinant only implements 2D"""
        if len(self) != 2 or len(vector) != 2:
            raise NotImplementedError
        return self[0] * vector[1] - self[1] * vector[0]

    @property
    def length(self) -> float:
        return math.sqrt(self.dot(self))

    @property
    def unit(self) -> Vector:
        return self / self.length

    def angle(self, vector) -> float:
        if((self.length * vector.length)==0): 
            return math.degrees(math.acos(self.dot(vector) / 1))
        else: 
            return math.degrees(math.acos(self.dot(vector) / (self.length * vector.length)))

    def signed_angle(self, vector) -> float:
        return math.degrees(math.atan2(self.det(vector), self.dot(vector)))

    def __add__(self, other) -> Vector:
        return Vector([a + b for a, b in zip(self, other)])

    def __sub__(self, other) -> Vector:
        return Vector([a - b for a, b in zip(self, other)])

    def __mul__(self, value: float) -> Vector:
        return Vector([x * value for x in self])

    def __rmul__(self, value: float) -> Vector:
        return self.__mul__(value)

    def __truediv__(self, value: float) -> Vector:
        return Vector([x / value for x in self])
        

class Keypoints(List[Point]):
    #AKA. Body25 without confidence. To see more detail,you can click the link 
    #https://drive.google.com/file/d/1JPoAzpX74uv0zMgTMUtrrO9GG6Epk6YM/view?usp=sharing
    # TODO: Consider confidence for higher accuracy
    # person_id:int
    face: List[Point]
    hand_left: List[Point]
    hand_right: List[Point]
    

    def __init__(self, points: List[Point], **kwargs: dict):
        
        super().__init__(points)
        
        #key: face;hand_left;hand_ringht...
        #value: (point,point,points)
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        #new code     
        self.left_th = self.left_thigh() 
        # print(points)
                   
    @classmethod
    def from_json(cls, path: str) -> Keypoints:
        """read the json file path which is Openpose write json to keypoints 
        json file have the skeleton, then change the skeleton to Dict datatype 
        and it have the 
        Augments: path :each json file path in specific folder 
        Return :
        """
        people: List[Dict[str, List[float]]] = load(open(path, encoding="utf-8"))[
            "people"
        ]
        
        if not people:
            # NOTE: generate empty person or use previous one
            raise EmptyPeopleError()
        # TODO: check person id
        # print(len(people[0]["pose_keypoints_2d"]))

        return  cls(  
                    Point.from_sequence(people[0]["pose_keypoints_2d"]),
                    face=Point.from_sequence(people[0]["face_keypoints_2d"]),
                    hand_left=Point.from_sequence(people[0]["hand_left_keypoints_2d"]),
                    hand_right=Point.from_sequence(people[0]["hand_right_keypoints_2d"]),
                    person_id = people[0]["person_id"],#直接在這裡宣告 person_id
                )

    @classmethod 
    def from_list(cls,seperated_person:list)->Keypoints:
        """ using the list data to generate Keypoints class
            like the from_json classmethod function 
        Arguments:
            seperated_person:(list):only one person list
        Return:
            cls function will auto constructe the Keypoints class 
        """

        people = seperated_person
        # print(people["pose_keypoints_2d"])
        
        return  cls(  
                    Point.from_sequence(people["pose_keypoints_2d"]),
                    face=Point.from_sequence(people["face_keypoints_2d"]),
                    hand_left=Point.from_sequence(people["hand_left_keypoints_2d"]),
                    hand_right=Point.from_sequence(people["hand_right_keypoints_2d"]),
                    person_id = people["person_id"],
                )                 

    @property
    def angles(self) -> List[float]:
        """AKA. Angle24"""
        return body25_to_angle24(self)

    def get_arc(self, point_idx: int) -> List[Point]:
        """Get arc from specific point index (body25)

        Args:
            point_idx (int): Body25 point

        Raises:
            ValueError: When this point is more than one angle

        Returns:
            [Point]: 3 points that can 
        """
        g = get_graph()
        adj_idxs = list(g.adj[point_idx])
        if not len(adj_idxs) == 2:
            raise ValueError(f"{point_idx} is not a correct index!")

        p = self[point_idx]
        p1 = self[adj_idxs[0]]
        p2 = self[adj_idxs[1]]
        return [p, p1, p2]

    @property
    def height(self: list) -> float:
        """畫面中的身高 (px)"""
        body = euclidean(self[8], self[1])
        
        leg = (
            euclidean(self[8], self[12])
            + euclidean(self[12], self[13])
            + euclidean(self[13], self[14])
        )
        # NOTE: Another method to evaluate person height still in experiments
        if False:
            face_half = euclidean(self.face[8], self.face[30])
            neck_and_face_half = euclidean(self[0], self[1])
            return body + leg + face_half + neck_and_face_half

        neck_to_head = euclidean(self[0], self[1]) * 1.8

        return body + leg + neck_to_head

    def bones(self):
        """將skeleton 轉換為骨頭長度"""
        return body_to_bones(self)
    
    def right_thigh(self):
        """右腳大腿骨"""
        return get_right_thigh(self)
    
    def left_thigh(self):
        """左腳大腿骨"""
        return get_left_thigh(self)

    @property
    def direction(self) -> float:
        """Body direction, 0 means face to camera, 90: right, 180: back, -90: left

        Returns:
            float: -180 < d <= 180
        """
        v1 = Vector((self[22].x - self[11].x, self[22].y - self[22].y))
        v2 = Vector((self[19].x - self[14].x, self[19].y - self[14].y))
        v_sum = v1 + v2
        v_vertical = Vector((0, 1))
        # get angle between v_sum and v_0
        angle = -v_vertical.signed_angle(
            v_sum
        )  # with previous sub due to (0, 0) is left top
        if self[2].x > self[5].x:
            # 背面
            if angle > 0:
                angle = 180 - angle
            else:
                angle = -180 - angle
        return angle

    @property
    def body_area(self) -> float:
        return polygon_area([self[2], self[5], self[12], self[9]])

    def d(self, max: float) -> float:
        body_area = self.body_area
        if self.body_area > max:
            body_area = max
        angle = math.degrees(math.acos(body_area / max))
        v1 = Vector((self[15].x - self[17].x, self[15].y - self[17].y)).unit
        v2 = Vector((self[16].x - self[18].x, self[16].y - self[18].y)).unit
        v3 = Vector((self[22].x - self[11].x, self[22].y - self[11].y)).unit
        v4 = Vector((self[19].x - self[14].x, self[19].y - self[14].y)).unit
        v_sum = v1 + v2 + v3 + v4
        if self[2].x > self[5].x:
            # 背面
            angle = 180 - angle
        if v_sum[0] < 0:
            # 左邊
            angle = -angle
        return angle


def get_dimensions(seqs, varthresh) -> set:
    dimensions = set()
    for i, kps in enumerate(seqs):
        varSeq = np.var(kps)
        if varSeq > float(varthresh):
            dimensions.add(i)
    return dimensions


