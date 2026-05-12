import random
import numpy as np 
import math
import os, sys
import pickle


class DataProcessor:
    def determine_direction(scene_info: dict, food_score, food_pos, list) :
        #The vector is point from squid to food
        delta_fx = food_pos[0] - scene_info['self_x']
        delta_fy = food_pos[1] - scene_info['self_y']
        #The vector is point from opponent to squid
        delta_ox = scene_info['opponent_x'] - scene_info['self_x']
        delta_oy = scene_info['opponent_y'] - scene_info['self_y']
        
        distance_food = math.sqrt(math.pow(abs(delta_fx),2) + math.pow(abs(delta_fy),2))
        distance_opponent = math.sqrt(math.pow(abs(delta_ox),2) + math.pow(abs(delta_oy),2))
        #limit the distacnce within 200
        eachfood_info = []
        if(distance_food < 400):
            eachfood_info = [distance_food, food_score]

        #Ananalyze oppoenet
        opponent_info = []
        if distance_opponent < 200:
            opponent_score = 0
            if scene_info['self_lv']>scene_info['opponent_lv']:
                opponent_score = 10
            elif scene_info['self_lv']<scene_info['opponent_lv']:
                opponent_score = -10 
            opponent_info = [distance_opponent, opponent_score]  
            #print("opponent_info") 
            #print(opponent_info)
            
         #0:up 1:down 2:left 3:right
        if eachfood_info is not None and eachfood_info:
            if(delta_fy>0 and delta_fx>0):   
                if(abs(delta_fy) > abs(delta_fx)):#down
                    list[1].append(eachfood_info)
                else:#right
                    list[3].append(eachfood_info)
            elif(delta_fy>0 and delta_fx<0): 
                if(abs(delta_fy) > abs(delta_fx)):#down
                    list[1].append(eachfood_info)
                else:#left
                    list[2].append(eachfood_info)
            elif(delta_fy<0 and delta_fx<0): 
                if(abs(delta_fy) > abs(delta_fx)):#up
                    list[0].append(eachfood_info)
                else:#left
                    list[2].append(eachfood_info)
            elif(delta_fy<0 and delta_fx>0): 
                if(abs(delta_fy) > abs(delta_fx)):#up
                    list[0].append(eachfood_info)
                else:#right
                    list[3].append(eachfood_info)
        
        if opponent_info is not None and opponent_info:
            if(delta_oy>0 and delta_ox>0):   
                if(abs(delta_oy) > abs(delta_ox)):#down
                    list[1].append(opponent_info)
                else:#right
                    list[3].append(opponent_info)
            elif(delta_oy>0 and delta_ox<0): 
                if(abs(delta_oy) > abs(delta_ox)):#down
                    list[1].append(opponent_info)
                else:#left
                    list[2].append(opponent_info)
            elif(delta_oy<0 and delta_ox<0): 
                if(abs(delta_oy) > abs(delta_ox)):#up
                    list[0].append(opponent_info)
                else:#left
                    list[2].append(opponent_info)
            elif(delta_oy<0 and delta_ox>0): 
                if(abs(delta_oy) > abs(delta_ox)):#up
                    list[0].append(opponent_info)
                else:#right
                    list[3].append(opponent_info)
        
    def quantify(food_4direction_list):
        #0:up 1:down 2:left 3:right
        result = []
        for i, sublist in enumerate(food_4direction_list, start=1):
            sublist_sum = 0
            for j, array in enumerate(sublist, start=1):
                if len(array) > 0:  # Check if the array is not empty
                    #array_sum = array[0]
                    array_sum = DataProcessor.score(array[0], array[1])
                    #print(f"Sum of element {i} list, array {j}: {array_sum}")
                    sublist_sum += array_sum
                    
            result.append(sublist_sum)
            #print(f"Sum of element {i} list: {sublist_sum}")
        return result
        #print(result)
        
    def score(distance, base_score, scaling_factor=1):
        return base_score * scaling_factor / (distance + 1)
    
    def mapping(my_list):
        # Sort the list and get the sorted indices
        sorted_indices = sorted(range(len(my_list)), key=lambda x: my_list[x])
        # Reverse the sorted indices to get ranks in ascending order
        ranks = [sorted_indices.index(i) for i in range(len(my_list))]
        return ranks
        
class QLearning:
    
    def __init__(self, gamma=0.9):
        self.rewards = 0
    
        self.gamma = gamma
        self.num_actions = 4  
        # 0:up, 1:down, 2:left, 3:right
        self.Qform = np.zeros((4,4,4,4,4))
    
    def initialize(self):
        self.Qform = np.zeros((4,4,4,4,4))
        
        
    def getAction(self, state: list, epsilon):
        if np.random.uniform(0, 1) < epsilon:
            # Explore randomly
            return np.random.randint(self.num_actions)
        else:
            # Exploit learned values
            # Q is a 4X4X4X4X4 array
            return np.argmax(self.Qform[state[0], state[1], state[2], state[3]])
        
    def getReward(self, state: list, action):
        #get the index( the direction) of the highest value
        reward = 0
        if action == state.index(3):
            reward = 4
        elif action == state.index(2):
            reward = 3
        elif action == state.index(1):
            reward = 2
        elif action == state.index(0):
            reward = 1
        
        return reward
        
    def updateQtable(self, old_state: list, action, reward, new_state: list, alpha):
        Qvalue = 0
        Qvalue_func = lambda x: (1 - alpha) * self.Qform[old_state[0],old_state[1],old_state[2],old_state[3], x] + alpha * (reward + self.gamma * np.max(self.Qform[new_state[0], new_state[1], new_state[2], new_state[3]]))
        Qvalue = Qvalue_func(action)
        
        #print(Qvalue)
        self.Qform[old_state[0],old_state[1],old_state[2],old_state[3], action] = Qvalue
        #print(self.Qform[old_state[0],old_state[1],old_state[2],old_state[3], action])
        #print(self.Qform[old_state[0],old_state[1],old_state[2],old_state[3], action])
        #print(self.Qform)
        
    def getQtable(self):
        return self.Qform
    
    def outputQtable(self):
        save_path = "/Users/harris/MLGame/swimming-squid-battle/RL_Qtable"
        with open(save_path, "wb") as file:
            pickle.dump(self.Qform, file)