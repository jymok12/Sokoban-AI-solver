# Breadth first search: https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
# A* star: https://www.geeksforgeeks.org/a-search-algorithm/
# Some pieces of code were taken from this: http://www.cs.toronto.edu/~fbacchus/csc384/Assignments/A1/search.py
import heapq
from collections import deque
import os

class sspace:
    # abstract class 
    # aima-python
    n = 0
    def __init__(self, action, gval, parent):
        self.action = action
        self.gval = gval
        self.parent = parent
        self.index = sspace.n
        sspace.n = sspace.n + 1

    def actions(self):        
        raise Exception("Override")

    def result(self):
        raise Exception("Override")

    def goal_test(self):
        raise Exception("Override")

    def path_cost(self):
        s = self
        states = []
        while s:
            states.append(s)
            s = s.parent
        states.pop().goal_test()
        while states:
            print(" ==> ", end="")
            states.pop().goal_test()
        print("")
 
    def value(self):
        s = self.parent
        hc = self.result()
        while s:
            if s.result() == hc:
                return True
            s = s.parent
        return False
 
_BREADTH_FIRST = 0
_ASTAR = 1

# These values are import when performing breadth first and a star search
sum_of_hval_gval = 0
hval = 1
gval = 2

# Cycle checking is crucial as it is required for the search to run continuosly
# If not, the loop will only run once and not infinitely
_CC_NONE = 0
_CC_PATH = 1
_CC_FULL = 2

def _zero_hfn(state):
    return 0

def _f_function(state):
  return state.hval 

class Nodes:
    n = 0
    types = sum_of_hval_gval
    
    def __init__(self, state, hval, fval_function):
        self.state = state
        self.hval = hval
        self.gval = state.gval
        self.index = Nodes.n
        self.fval_function = fval_function
        Nodes.n = Nodes.n + 1

    def __lt__(self, node):
        if Nodes.types == sum_of_hval_gval:
            if (self.gval+self.hval) == (node.gval+node.hval):
                return self.gval > node.gval
            else: 
                return ((self.gval+self.hval) < (node.gval+node.hval))
        
        if Nodes.types == gval:
            return self.gval < node.gval
        if Nodes.types == hval:
            return self.hval < node.hval    
        
        return self.gval < node.gval

class Open:
    def __init__(self, sstrat):
        # priority queue: https://docs.python.org/3/library/heapq.html
        if sstrat == _BREADTH_FIRST:
            #use queue for OPEN (first in---earliest node not yet expanded---is first out)
            self.open = deque()
            self.insert = self.open.append
            self.extract = self.open.popleft
        elif sstrat == _ASTAR:
            #use priority queue for OPEN (first out is node with lowest fval = gval+hval)
            self.open = []
            Nodes.types = sum_of_hval_gval
            self.insert = heapq.heappush(self.open, node)
            self.extract = heapq.heappop(self.open) 

    def empty(self): 
        return not self.open

# https://artint.info/AIPython/aipython/searchGeneric.py
# aima-python
# activates the search algorithms that were implemented and the code below is used in the main function in result.py
class engine:
    def __init__(self, strategy = 'breadth_first', check = 'default'):
        self.set_strategy(strategy , check)
        self.trace = 0

    def initStats(self):
        Nodes.n = 0
        sspace.n = 1   
        self.ccheck_pruned = 0
        self.cost_bound_pruned = 0

    def get_strategy(self):
        if self.strategy == _BREADTH_FIRST: 
            rval = 'breadth_first'
        elif self.strategy == _ASTAR:
            rval = 'astar'     
  
        rval = rval + ' path '

        if self.ccheck == _CC_FULL: 
            rval = rval + 'full'

        return rval

    def set_strategy(self, s, cc = 'default'):
            if not s in ['breadth_first', 'astar']:
                print("")
            
            elif not cc in ['default', 'none', 'path', 'full']:
                print("")
            
            else:
                if cc == 'default' :
                    if s == 'breadth_first' :
                        self.ccheck = _CC_PATH
                    else:
                        self.ccheck = _CC_FULL
                elif cc == 'full': 
                    self.ccheck = _CC_FULL
            
            if s == 'breadth_first': 
                self.strategy = _BREADTH_FIRST
            elif s == 'astar': 
                self.strategy = _ASTAR            

    def init_search(self, initState, g_final, heuristic_final=_zero_hfn, fval_function=_f_function):
        self.initStats()
        if self.trace:
            initState.goal_test()
        
        self.open = Open(self.strategy)
        node = Nodes(initState, heuristic_final(initState), fval_function)      

        # https://realpython.com/python-dicts/
        if self.ccheck == _CC_FULL:
            self.cc_dictionary = dict() 
            self.cc_dictionary[initState.result()] = initState.gval
        
        self.open.insert(node)
        self.fval_function = fval_function
        self.g_final = g_final
        self.heuristic_final = heuristic_final

    def search(self, time=10, boundaries=None):

        goal_node = []

        self.search_start_time = os.times()[0]
        self.search_stop_time = None
        if time:
            self.search_stop_time = self.search_start_time + time
        goal_node = self.openingsearch(self.g_final, self.heuristic_final, self.fval_function, boundaries)

        if goal_node:
            return goal_node.state
        else:   
            print("Search Failed! No solution found.")
            return False

    def openingsearch(self, g_final, heuristic_final, fval_function, boundaries):
        while not self.open.empty():
            node = self.open.extract()
            if node.state.gval != node.gval:
                print("")
            elif g_final(node.state):
              return node
            elif self.ccheck == _CC_FULL:
                self.cc_dictionary[node.state.result()], node.gval
            elif self.ccheck == _CC_FULL and self.cc_dictionary[node.state.result()] < node.gval:
                continue
            
            actions = node.state.actions()

            for succ in actions:
                h_state = succ.result()

                if self.ccheck == _CC_FULL and h_state in self.cc_dictionary:
                    self.cc_dictionary[h_state], succ.gval

                if self.ccheck == _CC_FULL and h_state in self.cc_dictionary:
                    self.cc_dictionary[h_state], succ.gval

                if self.ccheck == _CC_PATH and succ.value():
                    print("\n")

                
                prune_succ = (self.ccheck == _CC_FULL and
                              h_state in self.cc_dictionary and
                              succ.gval > self.cc_dictionary[h_state]
                             ) or (
                              self.ccheck == _CC_PATH and
                              succ.value()
                             )

                if prune_succ :
                    self.ccheck_pruned = self.ccheck_pruned + 1                
                    continue
                
                succ_hval = heuristic_final(succ)

                self.open.insert(Nodes(succ, succ_hval, node.fval_function))

                if self.ccheck == _CC_FULL:
                    self.cc_dictionary[h_state] = succ.gval
                
        return False