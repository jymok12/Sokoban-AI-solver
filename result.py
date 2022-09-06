import os
from search import *
from sokoban import Sokoban, d, sokoban_goal_state 
from cases import Cases

def abs_value(num):
  if num < 0:
    return num * -1
  else:
    return num

# aima-python
# abs_value value is required for manhattan
# https://stackoverflow.com/questions/12526792/manhattan-distance-in-a
  # although in java, I was able to convert it to python for some parts of the code taken from the comments
def manhattan_distance(state):
    # initial heuristic value
    h=0 
    for b in state.boxes:
      number_of_boxes=state.boxes[b]
      if state.rules == None:
        #find closest stores (min_distance)
        min_distance = float("inf") 
        for stores in state.stores:
          distance = abs_value(stores[0]-b[0])+abs_value(stores[1]-b[1])
          if distance <= min_distance:
            min_distance=distance
      elif (len(state.rules[number_of_boxes])!=1): 
          # if there are multiple rules find the closest rule and convert frozen set to list
          min_distance = float("inf") 
          for i in range(len(state.rules[number_of_boxes])): #find closest rule
            rule = list(state.rules[number_of_boxes])
            rule = rule[i]
            distance = abs_value(rule[0]- b[0])+abs_value(rule[1]- b[1])
            if distance <= min_distance:
              min_distance=distance
              
      else: 
          #if there is only one rule, must go there.
          rule = list(state.rules[number_of_boxes])
          rule = rule[0]
          distance = abs_value(rule[0]-b[0])+abs_value(rule[1]-b[1])
          min_distance = distance
      h+=min_distance  #total heuristic.
      min_distance = float("inf") #reintialize for next iteration
    return h
  
def check(b,state,height,width,goals,key):

  #if box not in stores
  if b not in goals: #there may be none, or there may be some.
    x=b[0]
    y=b[1]
    
    left = (x-1,y)
    right = (x+1,y)
    top = (x,y-1)
    bottom = (x,y+1)
    l_obs = False
    r_obs = False
    up_obs = False
    down_obs = False
  
    if top in state.walls or top[1] < 0 or top in state.boxes:
      up_obs = True
    if bottom in state.walls or bottom[1] > (height - 1) or bottom in state.boxes:
      down_obs = True
    if left in state.walls or left[0] < 0 or left in state.boxes:
      l_obs = True
    if right in state.walls or right[0] > (width -1) or right in state.boxes:
      r_obs = True
    
    # starts with safe since we don't know what happens
    safe = False 
    
    # float('inf') stands for infinity: https://www.geeksforgeeks.org/python-infinity/ since there endless possiblities per environemnt
    # along any side walls, if any others, bad kind, no solution
    # Environment #1
    
    if b[0] == 0 or b[0] == (width-1):
      if up_obs or down_obs: 
        return float('inf')
        
      if state.rules != None:
        index = state.boxes[b]
        corrections = state.rules[index]
        for rule in corrections: 
        # along the left and right wall
        # safe if there is a goal within it or at the plotted coordinate
          if b[0] == 0 and rule[0] == 0:
            safe = True
          if b[0] == (width-1) and rule[0] == (width-1):
            safe = True
        # unsafe therefore the loop will be restarted to the next one, testing each one until a solution can be found or not
        if safe == False:
          return float('inf')
          
      elif state.rules == None: #boxes can go in any of the storess.
        #therefore, we can check if any of the storess are along  the wall, if so, safe.
        for stores in state.stores:
          #along the top and bottom wall
          if b[0] == 0 and stores[0] == 0:
            safe = True
          if b[0] == (width-1) and stores[0] == (width-1):
            safe = True
        if safe == False:
          return float('inf')

        
    # Environment #2 
    # along the top and bottom walls. 
    elif b[1]==0 or b[1] == (height-1): 
      if l_obs or r_obs: 
        # if any on left or right, bad. 
        return float('inf')
        
      elif state.rules == None: # boxes can go in any of the stores
        for stores in state.stores:
          # checks if there is a goal on top
          if b[1] == 0 and stores[1] == 0:
            safe = True
          elif b[1] == (height-1) and stores[1] == (height-1):
            safe = True
        if safe == False:
          return float('inf')

      elif state.rules != None:  
        index = state.boxes[b]
        corrections = state.rules[index]
        for rule in corrections:
          # checks if the goal is at the bottom
          if b[1] == 0 and rule[1] == 0:
            safe = True
          elif b[1] == (height-1) and rule[1] == (height-1):
            safe = True
        if safe == False:
          return float('inf')
          
    if top in state.walls or top[1] < 0:
      up_obs = True
    if bottom in state.walls or bottom[1] > (height - 1):
      down_obs = True
    if left in state.walls or left[0] < 0:
      l_obs = True
    if right in state.walls or right[0] > (width -1):
      r_obs = True

    # returns infinity if the box is not at the goal depending on where the obstacle is
    if up_obs and r_obs:
      return float('inf')
    elif r_obs and down_obs:
      return float('inf')
    elif down_obs and l_obs:
      return float('inf')
    elif l_obs and up_obs:
      return float('inf') 

    if top in state.walls or top[1] < 0 or top in state.boxes:
      up_obs = True
    elif bottom in state.walls or bottom[1] > (height - 1) or bottom in state.boxes:
      down_obs = True
    elif left in state.walls or left[0] < 0 or left in state.boxes:
      l_obs = True
    elif right in state.walls or right[0] > (width -1) or right in state.boxes:
      r_obs = True
    
    # testing the corners of a sokoban board
    b_l_corner = (x-1,y+1)
    b_r_corner = (x+1,y+1)
    t_l_corner = (x-1,y-1)
    t_r_corner = (x+1,y-1)
   
    if l_obs and down_obs and b_l_corner in state.walls:
      return float('inf')
    if r_obs and down_obs and b_r_corner in state.walls:
      return float('inf')
    if l_obs and up_obs and t_l_corner in state.walls:
      return float('inf')
    if r_obs and up_obs and t_r_corner in state.walls:
      return float('inf')

  return 0 

def f_function(sN, quantity):
    return sN.gval + quantity * sN.hval

    
def target_a(initial_state, heuristic_final, quantity=1., time = 10):
    best_path_cost = float("inf")
    # setted an 8 second time limit per case
    time_left = 8
    iter = 0 
    
    total_fval = (f_function(sN, quantity))
    s = SearchEngine('breadth_first', 'full')
    s.init_search(initial_state, sokoban_goal_state, heuristic_final, total_fval)
    
    while (time_left > 0) and not s.open():
      iter += 1
      t_start = os.times()[0]
      
      if iter == 1:
        final = s.search(time)
        time_left = 8 - t_start 

      else: 
        cost = (float("inf"), float("inf"),best_path_cost) 
        final = s.search(time, cost)
        time_left = 8 - t_start 
            
      return final
    
    return False

def target(initial_state, heuristic_final, time = 10):
    best_path_cost = float("inf")
    time_left = 8
    iter = 0
    
    s = SearchEngine('breadth_first', 'full')
    s.init_search(initial_state, g_final = sokoban_goal_state, heuristic_final=heuristic_final)
    
    while (time_left > 0) and not s.open():
      iter += 1
      t_start = os.times()[0]
      print(t_start)
        
      if iter == 1:
        final = s.search(time)
      
        time_left = 8 - t_start 
      
      else:
        cost = (best_path_cost, float('inf'), float('inf'))
        final = s.search(time, cost)
        
        time_left = 8 - t_start 
            
      return final

# main function for the entire sokoban
if __name__ == "__main__":
  solved = 0; unsolved = []; counter = 0; time = 2; 
  print("Sokoban Solver")     
  print ("\n")

  for i in range(0, 10): 
    print("PROBLEM ", i)
    
    s0 = Cases[i] 

    # engine taken from search.py
    s = engine('breadth_first', 'full')
    s.init_search(s0, g_final = sokoban_goal_state, heuristic_final = manhattan_distance)
    final = s.search(time)

    if final:
      final.path_cost()
      solved += 1
    else:
      unsolved.append(i)    
    counter += 1

  print("\n")  
  print( solved," of ", counter ,"case(s)" , " has been solved in less than", time, "seconds.")
  print("Cases remained unsolved: ", unsolved)
  print("\n") 




