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
color_apple_normal = [1, 0, 0]  # 0 / 16
color_apple_cut = [1, 0.25, 0]  # 1
color_apple_grasped = [1, 0.5, 0]  # 2
color_apple_reached = [1, 0.8, 0]  # 3

color_knife_reaching = [0.5, 1, 0]  # 5
color_knife_cutting = [0.3, 1, 0]  # 6
color_knife_normal = [0, 1, 0]  # 7
color_knife_grasped = [0, 1, 0.3]  # 8
color_knife_reached = [0, 1, 0.6]  # 9

color_hand_reaching = [0, 0.6, 1]  # 12
color_hand_grasping = [0, 0.3, 1]  # 13
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

    # change color while moving as quick fix
    getfield_hand_col.setSFColor(color_hand_reaching)
    getfield_knife_col.setSFColor(color_knife_reached)

    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < n_step):
        get_hand_pos = [get_hand_pos[0] + dx, get_hand_pos[1], get_hand_pos[2] + dz]
        getfield_hand_pos.setSFVec3f(get_hand_pos)
        counter += 1


def hand_grasp_knife(inter_step=300):
    # for user
    print("hand grasps the knife")

    # inst. change, but induce arbitrary order
    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < inter_step):
        counter += 1
    getfield_hand_col.setSFColor(color_hand_grasping)
    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < inter_step):
        counter += 1
    getfield_knife_col.setSFColor(color_knife_grasped)



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

    getfield_knife_col.setSFColor(color_knife_reaching)
    getfield_apple_pos.setSFColor(color_apple_reached)

    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < n_step):
        # hand moves together with the knife
        get_hand_pos = [get_hand_pos[0] + dx, get_hand_pos[1], get_hand_pos[2] + dz]
        getfield_hand_pos.setSFVec3f(get_hand_pos)
        get_knife_pos = [get_knife_pos[0] + dx, get_knife_pos[1], get_knife_pos[2] + dz]
        getfield_knife_pos.setSFVec3f(get_knife_pos)
        counter += 1


def knife_cut_apple(inter_step=300):
    print("knife cuts the apple")

    # inst. change, but induce arbitrary order
    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < inter_step):
        counter += 1
    getfield_knife_col.setSFColor(color_knife_cutting)
    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < inter_step):
        counter += 1
    getfield_apple_col.setSFColor(color_apple_cut)


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


