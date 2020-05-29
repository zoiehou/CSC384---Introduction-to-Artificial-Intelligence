#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os #for time functions
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems

def sokoban_goal_state(state):
  '''
  @return: Whether all boxes are stored.
  '''
  for box in state.boxes:
    if box not in state.storage:
      return False
  return True

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.

    #Variables Initialization
    boxes_list = state.boxes
    storage_list = state.storage
    matt_dis = 0
    min_num = 0
    num_list = []

    #Check Manhattan distances
    for items in boxes_list:
        x1 = items[0]
        y1 = items[1]
        for goals in storage_list:
            x2 = goals[0]
            y2 = goals[1]
            num = (abs(x1-x2)+abs(y1-y2))
            num_list.append(num)
        min_num = min(num_list)
        matt_dis = matt_dis + min_num
        num_list = []
    return matt_dis


#SOKOBAN HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
  count = 0
  for box in state.boxes:
    if box not in state.storage:
        count += 1
  return count

#Function to test if list is empty
def is_not_empty(lists):
    if lists == []:
        return False
    else:
        return True

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.

    #Variables Initialization
    count = 0
    distance = 0
    min_dist = 0
    boxes_list = state.boxes
    robots_list = state.robots
    boxes_available = list(state.boxes - state.storage)
    storages_available = list(state.storage - state.boxes)
    dist_list = []
    num_list = []

    #Deadlock cost is high for distance (Aka. should not be selected for a next step)
    if has_deadlock(state):
        count += 200

    #Approx. how many steps
    count += trivial_heuristic(state)

    #Check approx. distance from robots to boxes using original Manhattan distance func
    for b in boxes_list:
        bx = b[0]
        by = b[1]
        for r in robots_list:
            rx = r[0]
            ry = r[1]
            num = (abs(bx - rx) + abs(by - ry))
            num_list.append(num)
        min_num = min(num_list)
        distance += min_num
        num_list = []

    #Check approx. distance for available boxes to available storages
    for b in boxes_available:
        bx = b[0]
        by = b[1]
        for s in storages_available:
            sx = s[0]
            sy = s[1]
            dist = (abs(bx-sx)+abs(by-sy))
            dist_list.append((dist,b,s))
            dist_list = sorted(dist_list)
    while is_not_empty(dist_list):
        min_dist = dist_list.pop(0)
        distance += min_dist[0]
        dist_list = [dist for dist in dist_list if dist[1] != min_dist[1] and dist[2] != min_dist[2]]

    #Add the two types of distances into the total count of distance
    count += distance
    return count

def find_storage_x(s_list, box):
    for s in s_list:
        if s[0] == box[0]:
            return False
    return True

def find_storage_y(s_list, box):
    for s in s_list:
        if s[1] == box[1]:
            return False
    return True

#Function to check if there is a deadlock for the boxes and the potential movements
def has_deadlock(state):
    #Variables Initialization
    boxes_available = list(state.boxes - state.storage)
    storages_available = list(state.storage - state.boxes)
    has_boxes = is_not_empty(boxes_available)
    deadlock = False
    while has_boxes and not deadlock:
        b = boxes_available[0]
        #Check if box is at egdes or if box has obstacles around
        #Bottom left edge
        if ((b[0] == 0) or (b[0]+1, b[1]) in state.obstacles or (b[0]-1, b[1]) in state.obstacles) and \
                ((b[1] == 0) or (b[0], b[1]+1) in state.obstacles or (b[0], b[1]-1) in state.obstacles):
            deadlock = True
        #Bottom right edge
        elif ((b[0] == state.width -1) or (b[0]-1, b[1]) in state.obstacles or (b[0]+1, b[1]) in state.obstacles) and \
                ((b[1] == 0) or (b[0], b[1]+1) in state.obstacles or (b[0], b[1]-1) in state.obstacles):
            deadlock = True
        #Top right edge
        elif ((b[0] == state.width-1) or (b[0]-1, b[1]) in state.obstacles or (b[0]+1, b[1]) in state.obstacles) and \
                ((b[1] == state.height-1) or (b[0], b[1]-1) in state.obstacles or (b[0], b[1]+1) in state.obstacles):
            deadlock = True
        #Top left edge
        elif ((b[0] == 0) or (b[0]+1, b[1]) in state.obstacles or (b[0]-1, b[1]) in state.obstacles) and \
                ((b[1] == state.height-1) or (b[0], b[1]-1) in state.obstacles or (b[0], b[1]+1) in state.obstacles):
            deadlock = True
        #Deadlock if box is at edge and no storage is available along the edge
        elif (b[0] == 0) and find_storage_x(storages_available, b):
            deadlock = True
        elif (b[1] == 0) and find_storage_y(storages_available, b):
            deadlock = True
        elif (b[0] == state.width - 1) and find_storage_x(storages_available, b):
            deadlock = True
        elif (b[1] == state.height - 1) and find_storage_y(storages_available, b):
            deadlock = True
        boxes_available.pop(0)
        #Check if list is empty
        has_boxes = is_not_empty(boxes_available)
    return deadlock

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    fval = sN.gval + weight*sN.hval
    return fval

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''

    #Variables Initialization
    final_sol = False
    start_time = os.times()[0]
    remaining_time = timebound
    costbound = (float('inf'), float('inf'), float('inf'))

    #Run it for the first time
    se = SearchEngine('custom', 'full')
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    se.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)
    sol = se.search(timebound)

    #Run to get better results
    while remaining_time > 0:
        if sol == False:
            return final_sol
        if sol.gval <= costbound[0]:
            remaining_time -= (os.times()[0] - start_time)
            start_time = os.times()[0]
            costbound = (sol.gval, sol.gval, sol.gval)
            final_sol = sol
        else:
            return final_sol
        sol = se.search(remaining_time, costbound)

    return final_sol

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''

    #Variables Initialization
    final_sol = False
    start_time = os.times()[0]
    remaining_time = timebound
    costbound = (float('inf'), float('inf'), float('inf'))

    #Run it for the first time
    se = SearchEngine('best_first', 'default')
    se.init_search(initial_state, sokoban_goal_state, heur_fn)
    sol = se.search(timebound)

    #Run to get better results
    while remaining_time > 0:
        if sol == False:
            return final_sol
        if sol.gval <= costbound[0]:
            remaining_time -= (os.times()[0] - start_time)
            start_time = os.times()[0]
            costbound = (sol.gval, float('inf'), float('inf'))
            final_sol = sol
        else:
            return final_sol
        sol = se.search(remaining_time, costbound)

    return final_sol
