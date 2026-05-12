import random
import numpy as np 
import math
import os, sys
import pickle

sys.path.append("/Users/harris/MLGame/swimming-squid-battle/ml")
# Now you can import modules from the appended directory
import ml.handleData as hd


class MLPlay:
    def __init__(self,*args, **kwargs):
        print("Initial ml script")

        self.pre_action = 0
        self.pre_reward = 0
        self.pre_state = [0,0,0,0]
        
        self.cur_action = 0
        self.cur_reward = 0
        self.cur_state = [0,0,0,0]
        self.Qform = np.zeros((4,4,4,4,4))
        self.round_num = 1
        
        initial_alpha = 1
        initial_epsilon = 1
        final_alpha = 0.01
        final_epsilon = 0.01
        self.total_rounds = 150
        
        self.epsilon_decay_func = lambda round_num: final_epsilon + (initial_epsilon - final_epsilon) * (1 - min(1.0, round_num / self.total_rounds))
        self.alpha_decay_func = lambda round_num: final_alpha + (initial_alpha - final_alpha) * (1 - min(1.0, round_num / self.total_rounds))
        self.qL = hd.QLearning()
        self.dataprocessor = hd.DataProcessor
        
    def update(self, scene_info: dict, *args, **kwargs): 
        #list of list for saving the food's position.
        #0:up 1:down 2:left 3:right
        food_4direction_list = [[] for _ in range(4)]

        foods_list = scene_info['foods'] 
        #divide food's position into four directions and sorted up from nearest to fartherest 
        for food in foods_list:
            food_pos = np.array([(food['x']),(food['y'])])
            food_score = (food['score'])
            self.dataprocessor.determine_direction(scene_info, food_score, food_pos, food_4direction_list)
        
        
        map_data = self.dataprocessor.mapping(self.dataprocessor.quantify(food_4direction_list))
        #print(map_data)
        self.cur_state = map_data
        #print(self.cur_state)
        epsilon = self.epsilon_decay_func(self.round_num)
        alpha = self.alpha_decay_func(self.round_num)
        
        self.cur_action = self.qL.getAction(self.cur_state, epsilon)
        #print(self.cur_action)
        self.cur_reward = self.qL.getReward(self.cur_state, self.cur_action)
            
        self.qL.updateQtable(self.cur_state, self.cur_action, self.cur_reward, self.pre_state, alpha)        
                
        self.pre_state = self.cur_state 
        self.pre_action = self.cur_action
        self.pre_reward =  self.cur_reward
        
        final_action = ""
        if self.cur_action == 0:
            final_action = "UP"
        elif self.cur_action == 1:
            final_action = "DOWN"
        elif self.cur_action == 2:
            final_action = "LEFT"
        elif self.cur_action == 3:
            final_action = "RIGHT"
            
        #print(final_action)
        
        #actions = ["UP", "DOWN", "LEFT", "RIGHT"]
        #return random.sample(actions, 1)
        if self.round_num == self.total_rounds:
            self.qL.outputQtable()
        
        #qL.showQtable
        return [final_action]
    
    def reset(self):
        #print("reset ml script")
        self.round_num += 1
        print("Round: "+str(self.round_num))
            
        pass
