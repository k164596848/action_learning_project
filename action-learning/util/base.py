import math
from glob import glob
from itertools import groupby
from typing import Iterable
from warnings import warn
from scipy.spatial.distance import euclidean
import networkx as nx
import math
import numpy as np



def consecutive_one(data: Iterable[bool]) -> int:
    """Returns longest 1 length"""
    data = list(data)
    if not any(data):
        return 0
    return max(sum(1 for _ in run) for val, run in groupby(data) if val)

def get_files_from_prefix(prefix: str, ext="json"):
    """讀取該個資料夾裡的所有json files path 並把path存入 list中  """
    files = sorted(glob(prefix + "*" + f".{ext}"))
    # print(files[0]," ,from func [get_files_from_prefix]")
    if not files:
        raise ValueError(f"{prefix} folder is empty!")
    return files

def separate_people(person:list,people_num:int):
    """將正確的人數分配完成。使用 x_position排序 來拆分人數，越右邊的人最先 。notice:影片中的人物請不要出現交錯與重疊現象\n
    Args:
        person{Person->list}:
    Return:list, and the length of list is equal to person number,which means it multiple daimension
    """
    #generate the empyt list
    separated_people =[[] for _ in range(people_num)]
    #put each people in the separated_people list
    for i in range(0,people_num): separated_people[i].append(person[i])
    
    for j in range(people_num,len(person),people_num):
        
        origin_p =[]
        
        [origin_p.append((person[n]['pose_keypoints_2d'][0:1])) for n in range(j,j+people_num)]

        origin_p = np.array(origin_p)[:,0]#change datatype to array and reduce daimantion
        origin_p = list(origin_p)#change datatype to list

        sorted_p  = sorted(origin_p,reverse = True)
       
       # j+what,j value +0 or +1 or +2.....
        for i in range(0,people_num):
            what = origin_p.index(sorted_p[i])
            separated_people[i].append(person[j+what])

        origin_p = []

    # print((seperated_people[0][-1]['pose_keypoints_2d'][0:2]))
    # print((seperated_people[1][-1]['pose_keypoints_2d'][0:2]))
    return separated_people

def get_angle(a: Iterable[float], b: Iterable[float], c: Iterable[float]):
    """三個點變成算角度"""
    # TODO: move to core    
    ang = math.degrees(#兩個向量的右邊角度
        math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    )    
    if (ang < 0 ):
        ang = ang + 360 
    else:
         ang 
    # NOTE: 轉換小角
    if ang > 180:
        ang = 360 - ang
    # print("側面ang  = ",ang)     
    return ang

def distance2angle(a: Iterable[float], b: Iterable[float], c: Iterable[float],thighMax:float):
    """正面換算角度 or 距離換算角度"""
    # TODO: move to core    
    
    delta_x=(c[0] - b[0])
    delta_y=(c[1] - b[1])
    # dist = math.hypot(delta_x, delta_y)
    dist=abs(delta_y)

    if (dist>thighMax): #大腿骨的max值
        thighMax = dist

    theta = math.degrees(#利用arcsin求 theta
        math.asin((delta_y/thighMax))
    )
           
    ang =180-(90-theta)
    # if(ang==180): print("d2a_ang==180")
    return ang

def get_similarity(a, b):
    """兩個角度算相似"""
    # TODO: move to core
    return math.cos(math.radians(abs(a - b)))

def body25_to_angle24(sequence: list):
    """Get angle24 from body25 seqeunce"""
    # warn("This method need to be refactor")
    # TODO: refactor it
    assert len(sequence) == 25 and len(sequence[0]) == 2
    angles = []
    angles.append(get_angle(sequence[0], sequence[1], sequence[2]))
    angles.append(get_angle(sequence[0], sequence[1], sequence[5]))
    angles.append(get_angle(sequence[2], sequence[1], sequence[8]))
    angles.append(get_angle(sequence[5], sequence[1], sequence[8]))
    angles.append(get_angle(sequence[1], sequence[2], sequence[3]))
    angles.append(get_angle(sequence[1], sequence[5], sequence[6]))
    angles.append(get_angle(sequence[2], sequence[3], sequence[4]))
    angles.append(get_angle(sequence[5], sequence[6], sequence[7]))
    angles.append(get_angle(sequence[1], sequence[8], sequence[9]))
    angles.append(get_angle(sequence[1], sequence[8], sequence[12]))
    angles.append(get_angle(sequence[8], sequence[9], sequence[10]))
    angles.append(get_angle(sequence[8], sequence[12], sequence[13]))
    angles.append(get_angle(sequence[9], sequence[10], sequence[11]))
    angles.append(get_angle(sequence[12], sequence[13], sequence[14]))
    angles.append(get_angle(sequence[10], sequence[11], sequence[24]))
    angles.append(get_angle(sequence[13], sequence[14], sequence[21]))
    angles.append(get_angle(sequence[22], sequence[11], sequence[24]))
    angles.append(get_angle(sequence[19], sequence[14], sequence[21]))
    angles.append(get_angle(sequence[11], sequence[22], sequence[23]))
    angles.append(get_angle(sequence[14], sequence[19], sequence[20]))
    angles.append(get_angle(sequence[1], sequence[0], sequence[15]))
    angles.append(get_angle(sequence[1], sequence[0], sequence[16]))
    angles.append(get_angle(sequence[0], sequence[15], sequence[17]))
    angles.append(get_angle(sequence[0], sequence[16], sequence[18]))
    return angles

def body_to_bones(skeleton: list):
    bones:dict = []
    bones={
        '左大腿骨': get_left_thigh(skeleton),
        '右大腿骨':get_right_thigh(skeleton),
        '脊椎骨':euclidean(skeleton[1],skeleton[0])
    }
        
    return  bones

def polygon_area(corners):
    """Get polygon area by using corners"""
    if not corners:
        return 0.0
    if len(corners[0]) != 2:
        raise NotImplementedError("Only for 2D keypoints")
    n = len(corners)  # of corners
    area = 0.0
    # Heron's formula
    for i in range(n):
        j = (i + 1) % n
        area += corners[i].x * corners[j].y
        area -= corners[j].x * corners[i].y
    area = abs(area) / 2.0
    return area

def get_graph() -> nx.Graph:
    """Openpose adjacency graph"""
    warn("nx.Graph need to be remove")
    g = nx.Graph()
    g.add_edge(15, 17)
    g.add_edge(15, 0)
    g.add_edge(16, 18)
    g.add_edge(0, 16)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(1, 8)
    g.add_edge(1, 5)
    g.add_edge(5, 6)
    g.add_edge(6, 7)
    g.add_edge(8, 9)
    g.add_edge(9, 10)
    g.add_edge(10, 11)
    g.add_edge(11, 24)
    g.add_edge(11, 22)
    g.add_edge(22, 23)
    g.add_edge(8, 12)
    g.add_edge(12, 13)
    g.add_edge(13, 14)
    g.add_edge(14, 19)
    g.add_edge(19, 20)
    g.add_edge(14, 21)
    return g

def get_right_thigh(sequence: list)-> float:
    """
    取得右腳大腿骨的值
    """
    try:
        right_x=(sequence[9].x - sequence[10].x)
        right_y=(sequence[9].y - sequence[10].y)
    except:
        right_x=(sequence[0][9].x - sequence[0][10].x)
        right_y=(sequence[0][9].y - sequence[0][10].y)
    right_thigh = math.hypot(right_x,right_y)

    return right_thigh

def get_left_thigh(sequence: list)-> float:
    """
    取得左大腿骨的值
    """
    # try:
    try:
        # print(len(sequence))
        # print((sequence))
        left_x =abs(sequence[12].x - sequence[13].x)
        left_y =abs(sequence[12].y - sequence[13].y)
    except:
        # print(len(sequence))
        # print(sequence)
        left_x =abs(sequence[0][12].x - sequence[0][13].x)
        left_y =abs(sequence[0][12].y - sequence[0][13].y)
        
    left_thigh_value = math.hypot(left_x,left_y)
    # except:
    #     print(sequence,"from base.py")

    return left_thigh_value

def convert_reliable_thighMax_list(windowsize:int,thigh_list:list) ->list:
    """
    將某一隻腳的大腿骨list 轉換到 穩定 MAX value list

    Args:
    windowsize(int):決定視窗的大小
    thigh_list(list):某一隻腳的大腿骨序列

    """
    reliable_thighMax =[]
    forward =int(windowsize/2)
    backward = int(windowsize/2)

    # print(thigh_list)
    for current in range(0,len(thigh_list)):
        winsize =[]         
        
        if (current <= windowsize):
            for i in range(0,windowsize):
                winsize.append(thigh_list[i])
        elif (current>=len(thigh_list)-windowsize):
            for j in range(current-windowsize,current):
                winsize.append(thigh_list[j])   
        else:
            for k in range(current-windowsize,current):
                winsize.append(thigh_list[k])
        
        #modify avg, give weight         
        winsize.sort(reverse=True)
        avg = (winsize[0]*0.1+winsize[1]*0.25+winsize[2]*0.3+winsize[3]*0.25+winsize[4]*0.1)               
        reliable_thighMax.append(avg)
            
    return reliable_thighMax 

def process_person():
    pass 