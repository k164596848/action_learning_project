from typing import List

import numpy as np

from core.action import Action
from core.base import Keypoints


def segment(action: Action, threashold=12, min_len=5) -> List[bool]:
    """[WIP] Segment a long action to action pisces by using angles evaluation

    Args:
        action (Action): An action
        threashold (int, optional): Defaults to 12 (We found this parameter by experience).
        min_len (int, optional): To make sure shortest length greator than {min_len}. Defaults to 5.

    Returns:
        List[bool]: bool list [True, True, ..., False, ...]
    """
    first = action[0].angles
    start = 0
    labels = [False]
    for frame in action[1:]:
        if start >= min_len and is_similar(frame.angles, first, threashold):
            labels.append(True)
            start = 0
        else:
            labels.append(False)
            start += 1
    return labels


def is_similar(angles1: List[float], angles2: List[float], threashold: float) -> bool:
    """Evaluate two angles list are similar or not by using MAE (Mean Absolute Error)

    Args:
        angles1 (List[float]): First angles list
        angles2 (List[float]): Second angles list
        threashold (float): 

    Returns:
        bool: 
    """
    assert len(angles1) == len(angles2)
    mae = np.mean(np.abs(np.array(angles1) - angles2))
    return mae <= threashold
