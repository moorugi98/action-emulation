"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Supervisor, Keyboard, Connector

# get the supervisor which is +alpha on the default Robot()
supervisor = Supervisor()
# get the time step of the current world
timestep = int(supervisor.getBasicTimeStep())

# grab handles
getfield_hand_pos = supervisor.getSelf().getField('translation')
getfield_apple_pos = supervisor.getFromDef('apple').getField('translation')
getfield_knife_pos = supervisor.getFromDef('knife').getField('translation')

get_hand_pos = getfield_hand_pos.getSFVec3f()
get_apple_pos = getfield_apple_pos.getSFVec3f()
get_knife_pos = getfield_knife_pos.getSFVec3f()

getfield_hand_col = supervisor.getFromDef("hand_appearance").getField("emissiveColor")
getfield_apple_col = supervisor.getFromDef("apple_appearance").getField("emissiveColor")
getfield_knife_col = supervisor.getFromDef("knife_appearance").getField("emissiveColor")

get_hand_col = getfield_hand_col.getSFColor()
get_apple_col = getfield_apple_col.getSFColor()
get_knife_col = getfield_knife_col.getSFColor()

# starting color
init_hand_color = [0, 0, 1]
init_apple_color = [1, 0, 0]
init_knife_color = [0.3, 1, 0]

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
    get_hand_col = init_hand_color
    get_apple_col = init_apple_color
    get_knife_col = init_knife_color
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


def hand_reach_knife(n_step=1000, eta=0.15):
    print("hand reaches the knife")
    global get_hand_pos
    dx = (get_knife_pos[0] - get_hand_pos[0]) / n_step
    dz = (get_knife_pos[2] - get_hand_pos[2]) / n_step
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
        get_hand_pos = [get_hand_pos[0] + dx, get_hand_pos[1], get_hand_pos[2] + dz]
        getfield_hand_pos.setSFVec3f(get_hand_pos)
        counter += 1


def hand_grasp_knife(n_step=1000):
    # for user
    print("hand grasps the knife")

    # compute change value
    global get_hand_col
    global get_knife_col
    hand_grasping_col = [0, 0.3, 1]
    knife_grasped_col = [0, 1, 0]
    dg_hand = (get_hand_col[1] - hand_grasping_col[1]) / n_step
    dr_knife = (get_knife_col[0] - knife_grasped_col[0]) / n_step

    # loop
    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < n_step):
        get_hand_col = [get_hand_col[0], get_hand_col[1] - dg_hand, get_hand_col[2]]
        getfield_hand_col.setSFColor(get_hand_col)
        get_knife_col = [get_knife_col[0] - dr_knife, get_knife_col[1], get_knife_col[2]]
        getfield_knife_col.setSFColor(get_knife_col)
        counter += 1


def knife_reach_apple(n_step=1000, eta=0.15):
    print("knife reaches the apple")
    global get_hand_pos
    global get_knife_pos
    dx = (get_apple_pos[0] - get_knife_pos[0]) / n_step
    dz = (get_apple_pos[2] - get_knife_pos[2]) / n_step
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
        # hand moves together with the knife
        get_hand_pos = [get_hand_pos[0] + dx, get_hand_pos[1], get_hand_pos[2] + dz]
        getfield_hand_pos.setSFVec3f(get_hand_pos)
        get_knife_pos = [get_knife_pos[0] + dx, get_knife_pos[1], get_knife_pos[2] + dz]
        getfield_knife_pos.setSFVec3f(get_knife_pos)
        counter += 1


def knife_cut_apple(n_step=1000):
    print("knife cuts the apple")
    # wanted color at the end
    cutting_knife_color = [0.6, 1, 0]
    cut_apple_color = [1, 0.3, 0]

    # rate of change per timestep
    global get_knife_col
    global get_apple_col
    dr_knife = (get_knife_col[0] - cutting_knife_color[0]) / n_step
    dg_apple = (get_apple_col[1] - cut_apple_color[1]) / n_step

    # loop
    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < n_step):
        get_knife_col = [get_knife_col[0] - dr_knife, get_knife_col[1], get_knife_col[2]]
        getfield_knife_col.setSFColor(get_knife_col)
        get_apple_col = [get_apple_col[0], get_apple_col[1] - dg_apple, get_apple_col[2]]
        getfield_apple_col.setSFColor(get_apple_col)
        counter += 1


def scenario_default():
    reset()
    pause()
    hand_reach_knife()
    pause()
    hand_grasp_knife()
    pause()
    knife_reach_apple()
    pause()
    knife_cut_apple()


scenario_default()


