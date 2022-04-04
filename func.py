# Import of 3rd party modules
import random
import numpy.random as np

def sym(symbol):
    """
    Converts a string into a symbol using unicode characters
    https://unicode-table.com/en/blocks/geometric-shapes/
    """
    switchcase = {
        "square":"\u25a0",
        "tridown":"\u25bc",
        "triright":"\u25ba",
        "disc":"\u25cf",
        "heart":"\u2665",
        "sword":"\u2694",
        "death":"\u2620"
    }
    
    return switchcase.get(symbol, "nothing")

def get_entry_lane(level):
    """
    Chooses the level entry lane based on a probability and level
    """
    lanes = [1,2,3]
    probabilities = [
        1 - 0.06 * (level-1),
        0 + 0.04 * (level-1),
        0 + 0.02 * (level-1)
    ]
    lane = np.choice(lanes, 1, p=probabilities)

    return lane

def get_entry_side(lane):
    """
    Decides the lane side for lanes 2 & 3
    """
    rand_num = random.randrange(1,3)
    if lane == 2:
        if rand_num > 1:
            side = 3 # lane 2 top
        else:
            side = 7 # lane 2 bottom
    elif lane == 3:
        if rand_num > 1:
            side = 1 # lane 3 top
        else:
            side = 9 # lane 3 bottom
    else:
        side = 5 # lane 1
    
    return side

def lane_to_xcoord(lane):
    """
    Converts the initial lane (side rather) to the x coordinate
    """
    return int((lane-1)/2)

def get_coords(coords):
    """
    Converts normalized coordinates to actual grid coordinates
    """
    result = [0,0]

    # x - lanes/rows
    result[0] = coords[0] * 2 + 1

    # y - columns
    result[1] = 7 + 4 * coords[1]

    return result

def get_path_options(prev_coords, coords, exclude_left, create_exit):
    """
    Decides on the amount of avail paths depending on the lane
    """
           
    lane = coords[0]
    row = coords[1]
    options = {}

    # probabilities
    if lane == 0:
        options["right"] = 0.3
        options["down"] = 0.4
        options["left"] = 0.3
    elif lane == 1:
        options["up"] = 0.2
        options["right"] = 0.25
        options["down"] = 0.3
        options["left"] = 0.25
    elif lane == 2:
        options["up"] = 0.25
        options["right"] = 0.25
        options["down"] = 0.25
        options["left"] = 0.25
    elif lane == 3:
        options["up"] = 0.3
        options["right"] = 0.25
        options["down"] = 0.2
        options["left"] = 0.25
    else: #lane == 4
        options["up"] = 0.4
        options["right"] = 0.3
        options["left"] = 0.3
        
    # option removal
    # going up
    if prev_coords[0] > coords[0]:
        del options["down"]
    # going down
    if prev_coords[0] < coords[0]:
        del options["up"]
    # going left
    if prev_coords[1] > coords[1]:
        del options["right"]
    # going right
    if prev_coords[1] < coords[1]:
        del options["left"]
    
    # can't go left
    if "left" in options and row == 0:
        del options["left"]
    # can't go right
    if "right" in options and row == 17 and create_exit == False:
        del options["right"]
    # can't go up
    if "up" in options and lane == 0:
        del options["up"]
    # can't go down
    if "down" in options and lane == 4:
        del options["down"]

    if "left" in options and exclude_left == True:
        del options["left"]

    key_to_list = list(options.keys())
    val_to_list = list(options.values())

    # add probability difference to remaining probabilities
    if len(val_to_list) < 4 and len(val_to_list) != 0:
        diff = (1 - sum(val_to_list)) / len(val_to_list)
        for i in range(len(val_to_list)):
            val_to_list[i] += diff

    #result = "right"
    if len(val_to_list) != 0:
        result = np.choice(key_to_list, 1, p=val_to_list)
    return result