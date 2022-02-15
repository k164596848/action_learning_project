from core.action import Action
from core.part import Part
import asyncio
from util.base import separate_people
from core.person import Person
import operator
from json import load
from typing import Dict, List, Union


def recoginition(tester):

    # the json file path need put into data table 
    
    # loading json file content
    path = "../action_learning_UI/vue_frontend/db.json"
    actions:List[Dict[str,str]]=load(open(path, encoding="utf-8"))["tasks"]
    action_candidate = {}
    for action in actions:
        # automatic generate the action compare item 
        coach = Action.from_json("../action_learning_UI/"+action["jsonpath"]+"/")[0:300]
        print(action["text"]+"generate Action calss success")
        compare_result = coach.compare(tester,weighted=True,weight = action["weight"])
        action_candidate[action["text"]]=float(compare_result[Part.FULL_BODY])

    # the dictionary structure to record the compare value a pick up the max action 
    return max(action_candidate, key=action_candidate.get)

# if __name__ ==  "__main__" :

#     tester  = Action.from_json("./tests/json/教練曲舉左/")[0:300]
#     activity_name = recoginition(tester)
#     print(activity_name)