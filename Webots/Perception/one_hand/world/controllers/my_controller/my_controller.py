"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Supervisor, Keyboard, Connector
import numpy as np

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

getfield_hand_col = supervisor.getFromDef("hand_appearance").getField("baseColor")
getfield_apple_col = supervisor.getFromDef("apple_appearance").getField("baseColor")
getfield_knife_col = supervisor.getFromDef("knife_appearance").getField("baseColor")

get_hand_col = getfield_hand_col.getSFColor()
get_apple_col = getfield_apple_col.getSFColor()
get_knife_col = getfield_knife_col.getSFColor()


getfield_hand_shape = supervisor.getFromDef("hand_mesh").getField("url")
getfield_hand_scale = supervisor.getFromDef("hand_solid").getField("scale")

# starting color
init_hand_color = [0, 0, 1]
init_apple_color = [1, 0.4, 0]
init_knife_color = [0.59, 1, 0]

# starting pos
init_hand_pos = [0.1, 0.2, 0.4]
init_apple_pos = [0.4, 0.2, -0.2]
init_knife_pos = [-0.5, 0.3, 0]


def pause(n_step=500):
    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < n_step):
        counter += 1


def reset():
    print("reset the simulation to initial condition")
    # set original color
    getfield_hand_col.setSFColor(init_hand_color)
    getfield_apple_col.setSFColor(init_apple_color)
    getfield_knife_col.setSFColor(init_knife_color)
    
    # set back to initial pos
    getfield_hand_pos.setSFVec3f(init_hand_pos)
    getfield_apple_pos.setSFVec3f(init_apple_pos)
    getfield_knife_pos.setSFVec3f(init_knife_pos)

    # set open hand
    getfield_hand_shape.setMFString(0,
                                    "/home/minseok/D/Uni/10/Masterarbeit/Main/Webots/Perception/one_hand/3dmodel/"
                                    "one_hand/hand_v1_L1.123c38c9cfe4-2d46-434b-995c-4f7cd8b7ab01/12683_hand_v1_FINAL.obj")
    getfield_hand_scale.setSFVec3f([0.003, 0.003, 0.003])


def hand_reach_knife(n_step, eta=300):
    print("hand reaches the knife")
    global get_hand_pos
    dx = (get_knife_pos[0] - get_hand_pos[0]) / (n_step + eta)
    dz = (get_knife_pos[2] - get_hand_pos[2]) / (n_step + eta)

    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < n_step):
        get_hand_pos = [get_hand_pos[0] + dx, get_hand_pos[1], get_hand_pos[2] + dz]
        getfield_hand_pos.setSFVec3f(get_hand_pos)
        counter += 1


def hand_grasp_knife():
    print("hand grasps the knife")
    getfield_hand_shape.setMFString(0,
        "/home/minseok/D/Uni/10/Masterarbeit/Main/Webots/Perception/one_hand/3dmodel/hand_folded/"
        "Hand_v2_L1.123c375ab4c6-0874-4531-aaf7-b165f7450ed2/11538_Hand_v2.obj")
    getfield_hand_scale.setSFVec3f([0.01, 0.01, 0.01])
    global get_hand_pos
    get_hand_pos = [get_hand_pos[0], get_hand_pos[1], get_hand_pos[2] - 0.1] # models don't align
    getfield_hand_pos.setSFVec3f(get_hand_pos)


def knife_reach_apple(n_step, eta=400):
    print("knife reaches the apple")
    global get_hand_pos
    global get_knife_pos
    dx = (get_apple_pos[0] - get_knife_pos[0]) / (n_step + eta)
    dz = (get_apple_pos[2] - get_knife_pos[2]) / (n_step + eta)

    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < n_step):
        # hand moves together with the knife
        get_hand_pos = [get_hand_pos[0] + dx, get_hand_pos[1], get_hand_pos[2] + dz]
        getfield_hand_pos.setSFVec3f(get_hand_pos)

        get_knife_pos = [get_knife_pos[0] + dx, get_knife_pos[1], get_knife_pos[2] + dz]
        getfield_knife_pos.setSFVec3f(get_knife_pos)

        counter += 1


def knife_cut_apple(n_step):
    print("knife cuts the apple")
    # wanted color at the end
    cutting_knife_color = [0.8, 1, 0]
    cut_apple_color = [1, 0.61, 0]

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
    hand_reach_knife(500, 200)
    pause()
    hand_grasp_knife()
    pause()
    knife_reach_apple(500, 300)
    pause()
    knife_cut_apple(500)


scenario_default()


