from search import *


class Sokoban(sspace):
    
    def __init__(self, action, gval, parent, width, height, player, boxes, stores, obstacles,
                 rules=None, box_colours=None, stores_colours=None):
        
        sspace.__init__(self, action, gval, parent)
        self.boxes = boxes

        self.width = width
        self.height = height

        self.player = player
        self.stores = stores

        self.obstacles = obstacles
        self.rules = rules
        
        self.box_colours = box_colours
        self.stores_colours = stores_colours

    def actions(self):

        actions = []
        transition_cost = 1
        # values that are used in the result

        for d in (UP, RIGHT, DOWN, LEFT):
            new_loc = d.move(self.player)
            
            if new_loc[0] < 0 or new_loc[0] >= self.width:
                continue
            if new_loc[1] < 0 or new_loc[1] >= self.height:
                continue
            if new_loc in self.obstacles:
                continue
            
            # helps to create the list for the boxes aka the object that needs to be moved
            new_boxes = dict(self.boxes)

            if new_loc in self.boxes:
                new_box_loc = d.move(new_loc)
                
                if new_box_loc[0] < 0 or new_box_loc[0] >= self.width:
                    continue
                if new_box_loc[1] < 0 or new_box_loc[1] >= self.height:
                    continue
                if new_box_loc in self.obstacles:
                    continue
                if new_box_loc in new_boxes:
                    continue
                
                index = new_boxes.pop(new_loc)
                new_boxes[new_box_loc] = index
            
            new_player = tuple(new_loc)

            new_state = Sokoban(action=d.name, gval=self.gval + transition_cost, parent=self,
                                     width=self.width, height=self.height, player=new_player,
                                     boxes=new_boxes, stores=self.stores, obstacles=self.obstacles,
                                     rules=self.rules, box_colours=self.box_colours,
                                     stores_colours=self.stores_colours)
            actions.append(new_state)

        return actions

    def result(self):
        return hash((self.player, frozenset(self.boxes.items())))

    # helps to identify what objects are moving based on color: https://gist.github.com/vratiu/9780109
    def state_string(self):
        # turns off the standard color of the terminal to contemplate for the markers in the sokoban board.
        disable_terminal_colouring = False
        r_colours = {
            'red': '\033[31m',
            'blue': '\033[34m',
            'yellow': '\033[33m',
            'normal': '\033[0m'
        }
        b_colours = {
            'red': '\033[41m',
            'blue': '\033[44m',
            'yellow': '\033[33m',
            'normal': '\033[0m'
        }

        # represnens the layout and placement of sokoban objects:
        # '#' is a wall
        # " " is a free space
        # "$" is a box
        # ". " is the goal
        # "x " is the boxes placed on a goal
        # ? is for sokoban

        map = []
        for y in range(0, self.height):
            row = []
            for x in range(0, self.width):
                row += [' ']
            map += [row]

        if self.stores_colours:
            if disable_terminal_colouring:
                for stores_point in self.stores:
                    map[stores_point[1]][stores_point[0]] = self.stores_colours[self.stores[stores_point]][0:1].upper()
            else:
                for stores_point in self.stores:
                    map[stores_point[1]][stores_point[0]] = b_colours[self.stores_colours[self.stores[stores_point]]] + '.' + b_colours['normal']
        else:
            for (i, stores_point) in enumerate(self.stores):
                map[stores_point[1]][stores_point[0]] = '.'
        for obstacle in self.obstacles:
            map[obstacle[1]][obstacle[0]] = '#'
        map[self.player[1]][self.player[0]] = '?'
        if self.box_colours:
            if disable_terminal_colouring:
                for box in self.boxes:
                    if box in self.stores:
                        if self.rules is None or box in self.rules[self.boxes[box]]:
                            map[box[1]][box[0]] = '$'
                        else:
                            map[box[1]][box[0]] = 'x'
                    else:
                        map[box[1]][box[0]] = self.box_colours[self.boxes[box]][0:1].lower()
            else:
                for box in self.boxes:
                    if box in self.stores:
                        if self.rules is None or box in self.rules[self.boxes[box]]:
                            map[box[1]][box[0]] = b_colours[self.stores_colours[self.stores[box]]] + r_colours[self.box_colours[self.boxes[box]]] + '$' + b_colours['normal']
                        else:
                            map[box[1]][box[0]] = b_colours[self.stores_colours[self.stores[box]]] + r_colours[self.box_colours[self.boxes[box]]] + 'x' + b_colours['normal']
                    else:
                        map[box[1]][box[0]] = r_colours[self.box_colours[self.boxes[box]]] + '*' + r_colours['normal']
        else:
            for box in self.boxes:
                if box in self.stores:
                    if self.rules is None or box in self.rules[self.boxes[box]]:
                        map[box[1]][box[0]] = '$'
                    else:
                        map[box[1]][box[0]] = 'x'
                else:
                    map[box[1]][box[0]] = '*'

        for y in range(0, self.height):
            map[y] = ['#'] + map[y]
            map[y] = map[y] + ['#']
        map = ['#' * (self.width + 2)] + map
        map = map + ['#' * (self.width + 2)]

        s = ''
        for row in map:
            for char in row:
                s += char
            s += '\n'

        return s        

    def goal_test(self):
        print("ACTION was " + self.action)      
        print(self.state_string())


def sokoban_goal_state(state):
  if state.rules is None:
    for box in state.boxes:
      if box not in state.stores:
        return False
    return True
  for box in state.boxes:
    if box not in state.rules[state.boxes[box]]:
      return False
  return True

# aima-python
# https://www.journaldev.com/22460/python-str-repr-functions
# https://www.programiz.com/python-programming/methods/built-in/hash
class d():
    def __init__(self, name, position):
        self.name = name
        self.position = position
    
  
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return self.__str__()
    
    def move(self, loc):
        return (loc[0] + self.position[0], loc[1] + self.position[1])

UP = d("up", (0, -1))
RIGHT = d("right", (1, 0))
DOWN = d("down", (0, 1))
LEFT = d("left", (-1, 0))



  
