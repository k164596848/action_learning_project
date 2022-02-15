from enum import Enum


class Activity(Enum):
    SIT_DOWN_AND_STAND_UP = "椅子坐立"
    # 2: ???
    RAISE_KNEE_IN_PLACE = "原地站立抬膝"
    SIT_FORWARD_ON_CHAIR = "椅子坐姿體前彎"
    EYES_OPEN_STAND_ON_FOOT = "開眼單足立"
    RAISE_HANDS = "肱二頭肌手臂屈舉"
