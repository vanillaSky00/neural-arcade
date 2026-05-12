import random
from pprint import pprint
import orjson
import pygame
import pickle
import os,sys
import numpy as np

sys.path.append("/Users/harris/MLGame/swimming-squid-battle/ml")
# Now you can import modules from the appended directory
import ml.handleData as hd


class MLPlay:
    def __init__(self,ai_name,*args,**kwargs):
        print("Initial ml script")
        with open('/Users/harris/MLGame/swimming-squid-battle/RL_Qtable', 'rb') as f:
           self.model = pickle.load(f)

        self.dataprocessor = hd.DataProcessor
    def update(self, scene_info: dict, keyboard:list=[], *args, **kwargs):   
        
        
        #datahandle
        foods_list = scene_info['foods'] 
        food_4direction_list = [[] for _ in range(4)]
        #divide food's position into four directions and sorted up from nearest to fartherest 
        for food in foods_list:
            food_pos = np.array([(food['x']),(food['y'])])
            food_score = (food['score'])
            self.dataprocessor.determine_direction(scene_info, food_score, food_pos, food_4direction_list)
        
        map_data = hd.DataProcessor.mapping(self.dataprocessor.quantify(food_4direction_list))
        
        action = np.argmax(self.model[map_data[0], map_data[1], map_data[2], map_data[3]])
        
        final_action = ""
        if action == 0:
            final_action = "UP"
        elif action == 1:
            final_action = "DOWN"
        elif action == 2:
            final_action = "LEFT"
        elif action == 3:
            final_action = "RIGHT"
        
        return [final_action]

    def reset(self):
        print("reset ml script")
        pass
