from sokoban import Sokoban

# Implements the grid locations for where the boxes, storage, obstacles, restrictions are located at the beginning before the AI solves it.
def plot_coordinates(x, x1, y, y1):

    points = []
    for i in range(x, x1):
        for j in range(y, y1):
            points.append((i, j))
    return points

# Test problems are referenced from this blog: https://sokoban-jd.blogspot.com/2015/09/sokoban-lessons-lines-5-8-boxes.html
# https://www.w3schools.com/python/ref_func_frozenset.asp
# frozenset ensures that these specific obstacles or restrictions do not move; are fixed coordinates
Cases = (
    # of all othese are cooridnates of where the boxes, storage areas and obstacles should be at and where some restricted areas are.
    Sokoban("START", 0, None, 4, 4, # dimensions
            (0, 3), #player
            {(1, 3): 0, (1, 2): 1}, #boxes
            {(2, 1): 0, (2, 2): 1}, #storage
            frozenset(((0, 0), (1, 0), (3, 3))), #obstacles
            (frozenset(((2, 1),)), frozenset(((2, 2),))), #restrictions,
            {0: 'red', 1: 'blue'}, #color of boxes
            {0: 'red', 1: 'blue'} #color of storages
            ),

    # Problem 1
    Sokoban("START", 0, None, 4, 5, # dimensions
            (0, 2), #player
            {(2, 2): 0, (3, 2): 1}, #boxes
            {(2, 1): 0, (3, 1): 1}, #storage
            frozenset(((0, 0), (4, 0), (2, 3), (3, 3), (4, 3))), #obstacles
            (frozenset(((3, 1),)), frozenset(((2, 1),))), #restrictions,
            {0: 'red', 1: 'blue'}, #color of boxes
            {1: 'red', 0: 'blue'} #color of storages
            ),

    # Problem 2
    Sokoban("START", 0, None, 6, 5, # dimensions
            (5, 4), #player
            {(1, 2): 0, (2, 2): 1}, #boxes
            {(2, 0): 0, (2, 3): 1}, #storage
            frozenset(((2, 1), (0, 0), (5, 0), (0, 3), (1, 3), (2, 3), (3, 3))), #obstacles
            (frozenset(((2, 0),)), frozenset(((2, 2),))), #restrictions,
            {0: 'red', 1: 'blue'}, #color of boxes
            {0: 'red', 1: 'blue'} #color of storages
            ),

    # Problem 3
    Sokoban("START", 0, None, 5, 5, # dimensions
            (2, 1), #player
            {(1, 1): 0, (1, 3): 1, (3, 1): 2, (3, 3): 3}, #boxes
            {(0, 0): 0, (0, 4): 1, (4, 0): 2, (4, 4): 3}, #storage
            frozenset(((1, 0), (2, 0), (3, 0), (1, 4), (2, 4), (3, 4))), #obstacles
            ),

    # Problem 4
    Sokoban("Start", 0, None, 6, 4, # dimensions
            (1, 0),
            {(1, 1): 0, (2, 1): 0, (3, 2): 0, (4, 1): 0, (5, 2): 0}, # boxes
            {(4, 0): 0, (5, 0): 0, (5, 1): 0, (5, 2): 0, (5, 3): 0}, # storages
            frozenset(((0, 0), (2, 0), (3, 0), (0, 3), (1, 3), (2, 3))), # obstacles
            ),

    # Problem 5
    Sokoban("START", 0, None, 6, 4, # dimensions
            (5, 3), #player
            {(3, 1): 0, (2, 2): 1, (3, 2): 2, (4, 2): 3}, #boxes
            {(0, 0): 0, (2, 0): 1, (1, 0): 2, (1, 1): 3}, #storage
            frozenset((plot_coordinates(4, 6, 0, 1)
                    + plot_coordinates(0, 3, 3, 4))), #obstacles
            (frozenset(((0, 0),)), frozenset(((2, 0),)), frozenset(((1, 0),)), frozenset(((1, 1),))), #restrictions,
            {0: 'red', 1: 'blue', 2: 'yellow', 3: 'red'}, #color of boxes
            {0: 'red', 1: 'blue', 2: 'yellow', 3: 'red'} #color of storages
            ),
    # Problem 6
    Sokoban("START", 0, None, 6, 4, # dimensions
            (5, 3), #player
            {(3, 1): 0, (2, 2): 1, (3, 2): 2, (4, 2): 3}, #boxes
            {(0, 0): 0, (2, 0): 1, (1, 0): 2, (1, 1): 3}, #storage
            frozenset((plot_coordinates(4, 6, 0, 1)
                    + plot_coordinates(0, 3, 3, 4))), #obstacles
            (frozenset(((0, 0),)), frozenset(((2, 0),)), frozenset(((1, 0),)), frozenset(((0, 0), (2, 0), (1, 0), (1, 1),))), #restrictions,
            {0: 'red', 1: 'blue', 2: 'yellow', 3: 'normal'}, #color of boxes
            {0: 'red', 1: 'blue', 2: 'yellow', 3: 'red'} #color of storages
            ),
    # Problem 7
    Sokoban("START", 0, None, 9, 6, # dimensions
            (0, 0), #player
            {(4, 3): 0, (6, 4): 1}, # Boxes
            {(1, 3): 0, (1, 5): 1}, # Storages
            frozenset((plot_coordinates(2, 7, 2, 3) + plot_coordinates(2, 3, 2, 6))), # obstacles
            None, #restrictions
            ),
    # Problem 8
    Sokoban("START", 0, None, 10, 7, # dimensions
            (0, 0), #player
            {(5, 3): 0, (7, 4): 1}, # Boxes
            {(1, 3): 0, (1, 6): 1}, # Storages
            frozenset((plot_coordinates(2, 8, 2, 3) + plot_coordinates(2, 3, 2, 7))), # obstacles
            None, #restrictions
            ),
    # Problem 9
    Sokoban("Start", 0, None, 6, 6, # dimensions
            (5, 5), #player
            {(3, 2): 0, (3, 3): 1, (3, 4): 2, (4, 3): 3}, # boxes
            {(0, 2): 0, (0, 3): 1, (0, 4): 2, (0, 5): 3}, # storages
            frozenset(((1, 2), (1, 3), (1, 4), (1, 5), (2, 2), (5, 1), (5, 0))), # obstacles
            None, # restrictions
            ),
    # Problem 10
    Sokoban("Start", 0, None, 6, 5, # dimensions
            (1, 4), #player
            {(4, 4): 0, (1, 2): 1, (4, 0): 3}, # boxes
            {(0, 4): 0, (5, 2): 1, (0, 0): 3}, # storages
            frozenset(), # no obstacles
            None
            ))

