from core.base import Keypoints, Point,EmptyPeopleError
from util.base import get_files_from_prefix
from json import load
from typing import List,Dict
import numpy as np


class Person(List):

    def __init__(self, *args,**kwargs:dict):
        super().__init__( *args,**kwargs)

        # print(kwargs)
        
        for key ,value in kwargs.items():
            setattr(self, key, value )
        


    @classmethod
    def get_json_content(cls,path:str,people_num=1,**kwargs):
        """read the all json file content in the floder.if want to caculate mutiple pepele please put the people number.  \n
        Args: [path](str):json files floder path. [pople_num](int):the defaut people number is 1. \n  
        Return: (list):all the keypoints informatin in the floder .\n
        """
        #open the floder 
        # select the json content 
        file_path = get_files_from_prefix(path,**kwargs)
        
        total_people=[]

        for path in file_path:
            people: List[Dict[str, List[float]]] = load(open(path, encoding="utf-8"))[
                "people"
            ]
            
            if not people:
                # NOTE: generate empty person or use previous one
                raise EmptyPeopleError()
            
            #save the json content as a list ,the length of list is  usally people_number*frames 
            for i in range (0,people_num):
                total_people.append(people[i])
            
            try:
                if(bool(people[people_num])):print("person 出現問題")
            except:
                pass
            # people_num = (len(people))
         
        return cls(
            list(total_people),
            people_num=len(people)
        )

    


