"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
import copy

from controller import Supervisor, Keyboard, Connector

# get the supervisor which is +alpha on the default Robot()
supervisor = Supervisor()
# get the time step of the current world
timestep = int(supervisor.getBasicTimeStep())

# grab handles
getfield_hand_pos = supervisor.getSelf().getField('translation')
getfield_apple_pos = supervisor.getFromDef('apple').getField('translation')
getfield_knife_pos = supervisor.getFromDef('knife').getField('translation')
getfield_object_pos = [getfield_hand_pos, getfield_knife_pos, getfield_apple_pos]

get_hand_pos = getfield_hand_pos.getSFVec3f()
get_apple_pos = getfield_apple_pos.getSFVec3f()
get_knife_pos = getfield_knife_pos.getSFVec3f()
get_freespace0_pos = [-0.6, 0.2, 0.5]
get_freespace1_pos = [0.7, 0.2, 0.5]
get_object_pos = [get_hand_pos, get_knife_pos, get_apple_pos, get_freespace0_pos, get_freespace1_pos]

getfield_hand_col = supervisor.getFromDef("hand_appearance").getField("emissiveColor")
getfield_apple_col = supervisor.getFromDef("apple_appearance").getField("emissiveColor")
getfield_knife_col = supervisor.getFromDef("knife_appearance").getField("emissiveColor")

get_hand_col = getfield_hand_col.getSFColor()
get_apple_col = getfield_apple_col.getSFColor()
get_knife_col = getfield_knife_col.getSFColor()

# starting color
color_apple_normal = [1, 0, 0]  # 0 / 16
# color_apple_cut = [1, 0.25, 0]  # 1
# color_apple_grasped = [1, 0.5, 0]  # 2
# color_apple_reached = [1, 0.8, 0]  # 3
color_apple_manipulated = [1, 0.8, 0]

# color_knife_reaching = [0.5, 1, 0]  # 5
# color_knife_cutting = [0.3, 1, 0]  # 6
color_knife_normal = [0, 1, 0]  # 7
# color_knife_grasped = [0, 1, 0.3]  # 8
# color_knife_reached = [0, 1, 0.6]  # 9

# color_hand_reaching = [0, 0.6, 1]  # 12
# color_hand_grasping = [0, 0.3, 1]  # 13
color_hand_normal = [0, 0, 1]  # 14


# starting pos
init_hand_pos = [0.1, 0.2, 0.4]
init_apple_pos = [0.4, 0.2, -0.2]
init_knife_pos = [-0.5, 0.3, 0]


def pause(n_step=200):
    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < n_step):
        counter += 1


def reset():
    print("reset the simulation to initial condition")
    # set original color
    global get_hand_col 
    global get_apple_col
    global get_knife_col
    get_hand_col = color_hand_normal
    get_apple_col = color_apple_normal
    get_knife_col = color_knife_normal
    getfield_hand_col.setSFColor(get_hand_col)
    getfield_apple_col.setSFColor(get_apple_col)
    getfield_knife_col.setSFColor(get_knife_col)
    
    # set back to initial pos
    global get_hand_pos
    global get_apple_pos
    global get_knife_pos
    get_hand_pos = init_hand_pos
    get_apple_pos = init_apple_pos
    get_knife_pos = init_knife_pos
    getfield_hand_pos.setSFVec3f(get_hand_pos)
    getfield_apple_pos.setSFVec3f(get_apple_pos)
    getfield_knife_pos.setSFVec3f(get_knife_pos)


def x_move_to_y(x_indices, y_index, n_step=1000, eta=0.15):
    print_x = []
    print_y = "None"
    for x_index in x_indices:
        if x_index == 0:
            print_x.append("Hand")
        elif x_index == 1:
            print_x.append("Knife")
        elif x_index == 2:
            print_x.append("Apple")
        else:
            raise ValueError("Invalid index")
    if y_index == 0:
        print_y = "Hand"
    elif y_index == 1:
        print_y = "Knife"
    elif y_index == 2:
        print_y = "Apple"
    elif y_index == 3 or y_index == 4:
        print_y = "Freespace"
    else:
        raise ValueError("Invalid index")
    print("{} moves near {}".format(print_x, print_y))

    list_obj_x = []  # for each x (moving) object
    for x_index in x_indices:
        obj_x = get_object_pos[x_index]
        list_obj_x.append(obj_x)
    obj_y = get_object_pos[y_index]
    dx = (obj_y[0] - list_obj_x[0][0]) / n_step  # just take the hand (list[0]) to calculate
    dz = (obj_y[2] - list_obj_x[0][2]) / n_step
    if dx < 0:
        dx += eta / n_step
    else:
        dx -= eta / n_step
    if dz < 0:
        dz += eta / n_step
    else:
        dz -= eta / n_step

    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < n_step):
        for i in range(len(x_indices)):
            list_obj_x[i] = [list_obj_x[i][0] + dx, list_obj_x[i][1], list_obj_x[i][2] + dz]
            getfield_object_pos[x_indices[i]].setSFVec3f(list_obj_x[i])
        counter += 1
    for i in range(len(x_indices)):
        get_object_pos[x_indices[i]] = copy.deepcopy(list_obj_x[i])


# def x_manipulate_y(y_index, inter_step=300):
#     # for user
#     print("hand grasps the knife")
#
#     # inst. change, but induce arbitrary order
#     getfield_hand_col.setSFColor(color_hand_grasping)
#     counter = 0
#     while (supervisor.step(timestep) != -1) and (counter < inter_step):
#         counter += 1
#     getfield_knife_col.setSFColor(color_knife_grasped)


reset()
x_move_to_y([0], 2)  # hand move_to apple
x_move_to_y([0], 1)  # hand move_to knife
# hand connect knife
x_move_to_y([0,1], 2)  # knife move_to apple
x_move_to_y([0,1], 3)  # knife move_to freespace 0
# hand release knife
x_move_to_y([0], 4)  # hand move_to freespace 1
