from os.path import exists
from typing import List

import cv2   
import numpy as np
from PIL import Image, ImageDraw

from core.base import Point

from .body import draw_arc,draw_arc_blue
from .util import text_with_border


class Video:
    def __init__(self, file_path, is_demo=False):
        self.check_file_exists(file_path)
        self.file_path = file_path
        self._info = None
        self._info_secs = None
        self._data = None
        self._arcs = None
        self._sec_arcs= None#this is for riase knee
        self.is_demo = is_demo

    @staticmethod
    def check_file_exists(path: str):
        if not exists(path):
            raise FileNotFoundError(path)

    def export(self, path: str,position, num:int =1):
        """Export video to specific path, before export video you should call methods
        `draw_arcs`, `draw_info`, ... first.

        Args:
            path (str): output path
            num (int) : people num
        """
        # FIXME: throw exception on out_path contains chinese and ext must be .mp4
        cap = cv2.VideoCapture(self.file_path)
        out = None
        current = 0
        while cap.isOpened():
            if out is None:
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                fps = cap.get(cv2.CAP_PROP_FPS)
                fourcc = cv2.VideoWriter_fourcc(*'H264')#指定編碼格式從 mp4v to H264
                out = cv2.VideoWriter(path, fourcc, round(fps), (int(width), int(height)))
                         
            ret, frame = cap.read()
            if not ret:
                break    

            last_frame = frame

            if self._data:
                if current < len(self._data):
                    data = self._data[current]
                else:
                    data = self._data[-1]
                count_position=(round(position[0])+150,round(position[1]))
                cv2.putText(
                    frame,
                    str(round(data, 2)),
                    count_position,#次數的位置
                    cv2.FONT_HERSHEY_SIMPLEX,
                    5,
                    (199, 153, 84),
                    5,
                )
            if self._arcs:
                if current < len(self._arcs):
                    arc = self._arcs[current]
                    #using the draw/body.py 
                    frame = draw_arc(frame, arc)

            if self._sec_arcs:#畫第二支腳
                if current<len(self._sec_arcs):
                    arc = self._sec_arcs[current]
                    frame = draw_arc_blue(frame,arc)
                    
            out.write(frame)
            current += 1

            if self.is_demo:
                cv2.imshow("frame", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        # Draw information
        
        if self._info and not last_frame is None:
            # write with information
            img_pil = Image.fromarray(last_frame)
            draw = ImageDraw.Draw(img_pil)
            info_position=(round(position[0])+150,round(position[1]))
            text_with_border(
                draw,
                info_position, #資訊的位置
                "\n".join([f"{k}: {v}" for k, v in self._info.items()])
            )
            img = np.array(img_pil)
        #TODO:need to reconstruct,fix the people number 
        if(num>1):#第二人
            [out.write(img) for _ in range(self._info_secs * 30)]
        else:
            # [out.write(img) for _ in range(self._info_secs * 30)]  
            [out.write(img) for _ in range(1)]   

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        # print(f"Export video h {height} ")
        # print(f"Export video w {width} ")
        # print(f"Export video fps {fps} ")
        print(f"Export video to {path} finish!")

    def draw_arcs(self, arcs: List[List[Point]]):
        self._arcs = arcs

    def draw_second_arcs(self,arcs:List[List[Point]]):
        self._sec_arcs = arcs

    def draw_data(self, data: List[float]):
        self._data = data
    
    def draw_info(self, info: dict, secs: int = 5):
        self._info = info
        self._info_secs = secs
