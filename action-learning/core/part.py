from __future__ import annotations

from enum import Enum, auto, unique
from typing import Dict


@unique
class Part(Enum):
    LEFT_SHOULDER = auto()
    RIGHT_SHOULDER = auto()
    LEFT_ARM = auto()
    RIGHT_ARM = auto()
    LEFT_LEG = auto()
    RIGHT_LEG = auto()
    BACKBONE = auto()
    BUTT = auto()
    FULL_BODY = auto()

 
    

    @staticmethod
    def to_body25(angle24: int) -> int:
        """Angle24 索引值轉換成 Body25 索引值

        Arguments:
            angle24 {int} -- Angle 24 索引值

        Returns:
            int -- Body 25 索引值
        """
        # TODO: Refactor it
        return [
            1,
            1,
            1,
            1,
            2,
            5,
            3,
            6,
            8,
            8,
            9,
            12,
            10,
            13,
            11,
            14,
            11,
            14,
            22,
            19,
            0,
            0,
            15,
            16,
        ][angle24]

    @staticmethod
    def to_json_seriable_dict(d: Dict[Part, float]) -> Dict[str, float]:
        return {key.name: val for key, val in d.items()}
