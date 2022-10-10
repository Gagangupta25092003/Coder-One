########################
###    Pathfinder    ###
########################
import numpy as np
class Node:

    def __init__(self, parent=None, location=None, action=None):
        self.parent = parent
        self.location = location
        self.action = action

        self.h = 0
        self.g = 0
        self.f = 0

def get_path(node):
    path = []

    while node.parent:
        path.append(node)
        node = node.parent

    return path

def get_path_actions(path):

    actions = []

    for node in path:
        actions.append(node.action)

    return actions

def astar(game_state, start, target):

        print("----A* STAR----")
        path = []

        # add starting node to open list
        open_list = [Node(None, start, None)]
        closed_list = []

        # exit the loop early if no path can be found
        # (the target is likely blocked off)
        max_loops = 500
        counter = 0

        # while lowest rank in OPEN is not the GOAL:
        while len(open_list) > 0 and counter <= max_loops:

            # find the node with the lowest rank
            curr_node = open_list[0]
            curr_index = 0

            for index, node in enumerate(open_list):
                if node.f < curr_node.f:
                    curr_node = node
                    curr_index = index

            # check-`1222 ` if this node is the goal
            if curr_node.location == target:
                print(f"~~~~~~~FOUND TARGET~~~~~~~")
                path = get_path(curr_node)
                return path

            # current = remove lowest rank item from OPEN
            # add current to CLOSED
            del open_list[curr_index]
            closed_list.append(curr_node)

            # get neighbors of current
            neighbors = get_free_neighbors(game_state, curr_node.location)
            neighbor_nodes = []
            for neighbor in neighbors:
                for location, action in neighbor.items():
                    neighbor_nodes.append(Node(None, location, action))

            #   for neighbors of current:
            for neighbor in neighbor_nodes:
                
                # used for loop behavior
                in_closed = False
                in_open = False

                # cost = g(current) + movementcost(current, neighbor)
                cost = curr_node.g + 1

                # if neighbor in OPEN and cost less than g(neighbor):
                #   remove neighbor from OPEN, because new path is better
                for index, node in enumerate(open_list):
                    if neighbor.location == node.location and cost < neighbor.g:
                        del open_list[index]
                        in_open = True

                # if neighbor in CLOSED and cost less than g(neighbor): ⁽²⁾
                #   remove neighbor from CLOSED
                for index, node in enumerate(closed_list):
                    if neighbor.location == node.location and cost < neighbor.g: 
                        del closed_list[index]
                        in_closed = True

                # if neighbor not in OPEN and neighbor not in CLOSED:
                #   set g(neighbor) to cost
                #   add neighbor to OPEN
                #   set priority queue rank to g(neighbor) + h(neighbor)
                #   set neighbor's parent to current
                if not in_open and not in_closed:
                    neighbor.g = cost
                    open_list.append(neighbor)
                    neighbor.h = manhattan_distance(neighbor.location, target)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = curr_node

            counter += 1
        print(f"---NO PATH FOUND---")

def astar_b(game_state, start, target, game_map):

    print("----A* STAR----")
    path = []

    # add starting node to open list
    open_list = [Node(None, start, None)]
    closed_list = []

    # exit the loop early if no path can be found
    # (the target is likely blocked off)
    max_loops = 500
    counter = 0

    # while lowest rank in OPEN is not the GOAL:
    while len(open_list) > 0 and counter <= max_loops:

        # find the node with the lowest rank
        curr_node = open_list[0]
        curr_index = 0

        for index, node in enumerate(open_list):
            if node.f < curr_node.f:
                curr_node = node
                curr_index = index

        # check-`1222 ` if this node is the goal
        x,y = curr_node.location
        if curr_node.location == target or game_map[y][x] == 0:
            print(f"~~~~~~~FOUND TARGET~~~~~~~")
            path = get_path(curr_node)
                
            return path

        # current = remove lowest rank item from OPEN
        # add current to CLOSED
        del open_list[curr_index]
        closed_list.append(curr_node)

        # get neighbors of current
        neighbors = get_free_neighbors(game_state, curr_node.location)
        neighbor_nodes = []
        for neighbor in neighbors:
            for location, action in neighbor.items():
                neighbor_nodes.append(Node(None, location, action))

        #   for neighbors of current:
        for neighbor in neighbor_nodes:
                
            # used for loop behavior
            in_closed = False
            in_open = False

                # cost = g(current) + movementcost(current, neighbor)
            cost = curr_node.g + 1

            # if neighbor in OPEN and cost less than g(neighbor):
            #   remove neighbor from OPEN, because new path is better
            for index, node in enumerate(open_list):
                if neighbor.location == node.location and cost < neighbor.g:
                    del open_list[index]
                    in_open = True

            # if neighbor in CLOSED and cost less than g(neighbor): ⁽²⁾
            #   remove neighbor from CLOSED
            for index, node in enumerate(closed_list):
                if neighbor.location == node.location and cost < neighbor.g: 
                    del closed_list[index]
                    in_closed = True

            # if neighbor not in OPEN and neighbor not in CLOSED:
            #   set g(neighbor) to cost
            #   add neighbor to OPEN
            #   set priority queue rank to g(neighbor) + h(neighbor)
            #   set neighbor's parent to current
            if not in_open and not in_closed:
                neighbor.g = cost
                open_list.append(neighbor)
                neighbor.h = manhattan_distance(neighbor.location, target)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = curr_node

        counter += 1
    print(f"---NO PATH FOUND---")

# given our current location, return only surrounding tiles that are free
def get_free_neighbors(game_state, location):

    x, y = location
    neighbors = [{(x-1, y): 'l'}, {(x+1, y): 'r'}, {(x, y-1): 'd'}, {(x, y+1): 'u'}]
    free_neighbors = []

    for neighbor in neighbors:
        for tile, direction in neighbor.items():    
            if game_state.is_in_bounds(tile):
                if game_state.is_occupied(tile):
                     # check if this tile contains treasure or ammo
                    if game_state.entity_at(tile) == 't' or game_state.entity_at(tile) == 'a':
                        free_neighbors.append({tile:direction})
                else:
                    free_neighbors.append({tile:direction})

    return free_neighbors

# returns the manhattan distance between two tiles, calculated as:
# 	|x1 - x2| + |y1 - y2|
def manhattan_distance(start, end):

    distance = abs(start[0] - end[0]) + abs(start[1] - end[1])

    return distance

# finds ammo, if any
def get_ammo(game_state):

    ammo = game_state.ammo

    return ammo # return first ammo on the list

# finds treasure, if any
def get_treasure(game_state):

    treasure = game_state.treasure

    if treasure:
        return treasure # return first treasure on the list

def bomb_places(location):
    x,y = location
    l = [(x,y),(x+1,y),(x+2,y),(x-1,y),(x-2,y),(x,y+1),(x,y+2),(x,y-1),(x,y-2)]
    return l

def enemy_nearplaces(e_location,p_location,game_state):
    x,y = e_location
    location = []
    if not game_state.is_occupied((x+1,y)):
        location.append((x+1,y))
    if not game_state.is_occupied((x-1,y)):
        location.append((x-1,y))
    if not game_state.is_occupied((x,y+1)):
        location.append((x,y+1))
    if not game_state.is_occupied((x,y-1)):
        location.append((x,y-1))

    for i in range(len(location)):
        for j in range(i,len(location)):
            if(manhattan_distance(location[i], p_location) > manhattan_distance(location[j], p_location)):
                target = location[i]
                location[i] = location[j]
                location[j] = target

    print(location)
    return (location)



def safe_place(game_state, p_location, game_map):
    pos = []
    rows = game_state.size[1]
    cols = game_state.size[0]
    for i in range(rows):
        for j in range(cols):
            if game_map[i][j] == 0 and manhattan_distance((j,i),p_location) == 1:
                pos.append((i,j))

    for i in range(rows):
        for j in range(cols):
            if game_map[i][j] == 0 and manhattan_distance((j,i),p_location) == 2:
                pos.append((i,j))

    for i in range(rows):
        for j in range(cols):
            if game_map[i][j] == 0 and manhattan_distance((j,i),p_location) == 3:
                pos.append((i,j))

    for i in range(rows):
        for j in range(cols):
            if game_map[i][j] == 0 and manhattan_distance((j,i),p_location) == 4:
                pos.append((i,j))

    for i in range(rows):
        for j in range(cols):
            if game_map[i][j] == 0 and manhattan_distance((j,i),p_location) == 5:
                pos.append((i,j))

    return pos

def anyoption(p_location, game_map, game_state):
    x,y = p_location
    togo = []
    pos =[]
    if game_state.is_in_bounds((x+1,y)):
        pos.append((x+1,y))
    if game_state.is_in_bounds((x-1,y)):
        pos.append((x-1,y))
    if game_state.is_in_bounds((x,y+1)):
        pos.append((x,y+1))
    if game_state.is_in_bounds((x,y-1)):
        pos.append((x,y-1))
    
    for i in pos:
        x,y = i
        if game_map[y][x] == 0:
            togo.append(i)

    return togo

def nextPosition(act,p_location):
    x,y = p_location
    if act == 'u':
        y = y+1
    if act == 'd':
        y = y-1
    if act == 'r':
        x = x+1
    if act == 'l':
        x = x-1
    l = (x,y)
    return l

def isnearenemy(e_location,p_location):
    x,y = e_location
    l = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]

    if p_location in l:
        return True
    else:
        return False

def get_unsafe_places(bombs,gamemap,game_state):
    for i in bombs:
        x,y = i
        if game_state.is_in_bounds((x,y-2)):
            y,x = i
            if gamemap[x-1][y] != 2 and gamemap[x-1][y] != 3 and gamemap[x-2][y] != 2 and gamemap[x-2][y] != 3:
                gamemap[x-2][y] = -1
        x,y = i
        if game_state.is_in_bounds((x,y+2)):
            y,x = i
            if gamemap[x+1][y] != 2 and gamemap[x+1][y] != 3 and gamemap[x+2][y] != 2 and gamemap[x+2][y] != 3:
                gamemap[x+2][y] = -1
        x,y = i
        if game_state.is_in_bounds((x-2,y)):
            y,x = i
            if gamemap[x][y-1] != 2 and gamemap[x][y-1] != 3 and gamemap[x][y-2] != 2 and gamemap[x][y-2] != 3:
                gamemap[x][y-2] = -1
        x,y = i
        if game_state.is_in_bounds((x+2,y)):
            y,x = i
            if gamemap[x][y+1] != 2 and gamemap[x][y+1] != 3 and gamemap[x][y+2] != 2 and gamemap[x][y+2] != 3:
                gamemap[x][y+2] = -1

        x,y = i
        if game_state.is_in_bounds((x,y-1)):
            y,x = i
            if gamemap[x-1][y] != 2 and gamemap[x-1][y] != 3:
                gamemap[x-1][y] = -1
        x,y = i
        if game_state.is_in_bounds((x,y+1)):
            y,x = i
            if gamemap[x+1][y] != 2 and gamemap[x+1][y] != 3 :
                gamemap[x+1][y] = -1
        x,y = i
        if game_state.is_in_bounds((x-1,y)):
            y,x = i
            if gamemap[x][y-1] != 2 and gamemap[x][y-1] != 3 :
                gamemap[x][y-1] = -1
        x,y = i
        if game_state.is_in_bounds((x+1,y)):
            y,x = i
            if gamemap[x][y+1] != 2 and gamemap[x][y+1] != 3 :
                gamemap[x][y+1] = -1
        x,y = i
        gamemap[y][x] = -1

    return gamemap
        


def print_map(self, game_state):
        cols = game_state.size[0]
        rows = game_state.size[1]
        game_map = np.zeros((rows, cols))
        for x in range(cols):
            for y in range(rows):
                entity = str(game_state.entity_at((x,y)))
                if entity == 'None' or entity == 't' or entity == '0' or entity == 'a':
                    game_map[y][x] = 0
                elif entity == '1':
                    game_map[y][x] = 1
                elif entity == 'sb':
                    game_map[y][x] = 2
                else:
                    game_map[y][x] = 3
                     
        return game_map
    
def move(pf_location,pi_location):
    print(f"pf location : {pf_location}")
    x,y = pi_location
    X,Y = pf_location
    if X-x == 1:
        return 'l'
    elif X-x == -1:
        return 'r'
    elif Y-y == 1:
        return 'd'
    else:
        return 'u'

def nmove(action,pi_location):
    x,y = pi_location
    if action == 'l':
        return (x-1,y)
    elif action == 'r':
        return (x+1,y)
    elif action == 'u':
        return (x,y+1)
    elif action == 'd':
        return (x,y-1)
    else:
        return (x,y)