from typing import List

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from core.base import Point, Vector


def draw_arc(frame: np.array, points: List[Point]) -> np.array:
    """Draw arc 畫角度 using 

    Args:
        frame (np.array): An image (2d array or 3d array (RGB))
        points (List[Point]): list of points

    Returns:
        np.array: [description]
    """
    img = Image.fromarray(frame)
    draw = ImageDraw.Draw(img)
    p = points[0]

    #change 11/05 
    # testx=float(points[0].x)
    # testy =float(points[0].y)
    # test = [testx,testy-100]
    # test2=Point(testx,testy-100,1)
    # print(type(test2),test2)
    
    # p1 = test2
    p1=points[1]

    p2 = points[2]
    draw.line((p, p1), "red", 5)
    draw.line((p, p2), "red", 5)
    
    v1 = Vector(p1 - p)
    v2 = Vector(p2 - p)
    r = min(v1.length, v2.length)
    v = Vector((1, 0))
    ang1 = v.signed_angle(v1)
    ang2 = v.signed_angle(v2)
    ang = v1.angle(v2) #this is the ang of the p2a
    reverse = v1.signed_angle(v2) < 0
    if reverse:
        ang1, ang2 = ang2, ang1
    draw.arc((p - r, p + r), ang1, ang2, "red", 5)

    

    font = ImageFont.truetype("./data/NotoSansCJKtc-Regular.otf", 40)
    draw.text(
        p - 5, r"{:f}°".format(ang), font=font, fill=(0, 255, 0, 255),
    )
    return np.asarray(img)

def draw_arc_blue(frame: np.array, points: List[Point]) -> np.array:
    """Draw arc 畫角度 using 

    Args:
        frame (np.array): An image (2d array or 3d array (RGB))
        points (List[Point]): list of points

    Returns:
        np.array: [description]
    """
    img = Image.fromarray(frame)
    draw = ImageDraw.Draw(img)
    p = points[0]

    #change 11/05 
    # testx=float(points[0].x)
    # testy =float(points[0].y)
    # test = [testx,testy-100]
    # test2=Point(testx,testy-100,1)
    # print(type(test2),test2)
    
    # p1 = test2
    p1=points[1]

    p2 = points[2]
    draw.line((p, p1), "blue", 5)
    draw.line((p, p2), "blue", 5)
    
    v1 = Vector(p1 - p)
    v2 = Vector(p2 - p)
    r = min(v1.length, v2.length)
    v = Vector((1, 0))
    ang1 = v.signed_angle(v1)
    ang2 = v.signed_angle(v2)
    ang = v1.angle(v2) #this is the ang of the p2a
    reverse = v1.signed_angle(v2) < 0
    
    if reverse:
        ang1, ang2 = ang2, ang1
    draw.arc((p - r, p + r), ang1, ang2, "blue", 5)

    

    font = ImageFont.truetype("./data/NotoSansCJKtc-Regular.otf", 40)
    draw.text(
        p - 5, r"{:f}°".format(ang), font=font, fill=(0, 255, 0, 255),
    )
    return np.asarray(img)


def draw_body(draw: ImageDraw.Draw, seqs, color="blue", width=5):
    """Draw body like OpenPose Body25

    Args:
        draw (ImageDraw.Draw): Pillow Draw object
        seqs (Iterable): A sequence with (x, y) coordinate
        color (str, optional): Color. Defaults to "red".
        width (int, optional): Width. Defaults to 5.
    """
    # TODO: refactor it
    draw.line((tuple(seqs[15]), tuple(seqs[17])), color, width)
    draw.line((tuple(seqs[15]), tuple(seqs[0])), color, width)
    draw.line((tuple(seqs[16]), tuple(seqs[18])), color, width)
    draw.line((tuple(seqs[0]), tuple(seqs[16])), color, width)
    draw.line((tuple(seqs[0]), tuple(seqs[1])), color, width)
    draw.line((tuple(seqs[1]), tuple(seqs[2])), color, width)
    draw.line((tuple(seqs[2]), tuple(seqs[3])), color, width)
    draw.line((tuple(seqs[3]), tuple(seqs[4])), color, width)
    draw.line((tuple(seqs[1]), tuple(seqs[8])), color, width)
    draw.line((tuple(seqs[1]), tuple(seqs[5])), color, width)
    draw.line((tuple(seqs[5]), tuple(seqs[6])), color, width)
    draw.line((tuple(seqs[6]), tuple(seqs[7])), color, width)
    draw.line((tuple(seqs[8]), tuple(seqs[9])), color, width)
    draw.line((tuple(seqs[9]), tuple(seqs[10])), color, width)
    draw.line((tuple(seqs[10]), tuple(seqs[11])), color, width)
    draw.line((tuple(seqs[11]), tuple(seqs[24])), color, width)
    draw.line((tuple(seqs[11]), tuple(seqs[22])), color, width)
    draw.line((tuple(seqs[22]), tuple(seqs[23])), color, width)
    draw.line((tuple(seqs[8]), tuple(seqs[12])), color, width)
    draw.line((tuple(seqs[12]), tuple(seqs[13])), color, width)
    draw.line((tuple(seqs[13]), tuple(seqs[14])), color, width)
    draw.line((tuple(seqs[14]), tuple(seqs[19])), color, width)
    draw.line((tuple(seqs[19]), tuple(seqs[20])), color, width)
    draw.line((tuple(seqs[14]), tuple(seqs[21])), color, width)
