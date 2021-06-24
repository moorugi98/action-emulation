"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Supervisor, Keyboard, Connector
import numpy as np

# get the supervisor which is +alpha on the default Robot()
supervisor = Supervisor()
# get the time step of the current world
timestep = int(supervisor.getBasicTimeStep())

# init stuff
hand_node = supervisor.getSelf()
apple_node = supervisor.getFromDef('apple')
knife_node = supervisor.getFromDef('knife')


def hand_reach_apple(n_step, eta=400):
    hand_pos_field = hand_node.getField('translation')
    hand_pos = hand_pos_field.getSFVec3f()
    apple_pos_field = apple_node.getField('translation')
    apple_pos = apple_pos_field.getSFVec3f()
    dx = (apple_pos[0] - hand_pos[0]) / (n_step + eta)  # hand shouldn't cover the apple
    dz = (apple_pos[2] - hand_pos[2]) / (n_step + eta)

    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < n_step):
        hand_pos = [hand_pos[0] + dx, hand_pos[1], hand_pos[2] + dz]
        hand_pos_field.setSFVec3f(hand_pos)
        counter += 1


def hand_cut_apple(n_step):
    # wanted color at the end
    cutting_hand_color = [0, 0.65, 1]
    cut_apple_color = [1, 0.61, 0]
    # current color
    hand_color_field = supervisor.getFromDef("hand_appearance").getField("baseColor")
    hand_color = hand_color_field.getSFColor()
    apple_color_field = supervisor.getFromDef("apple_appearance").getField("baseColor")
    apple_color = apple_color_field.getSFColor()
    # rate of change per timestep
    dg_hand = (hand_color[1] - cutting_hand_color[1]) / n_step
    dg_apple = (apple_color[1] - cut_apple_color[1]) / n_step

    # loop
    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < n_step):
        hand_color = [hand_color[0], hand_color[1] - dg_hand, hand_color[2]]
        hand_color_field.setSFColor(hand_color)
        apple_color = [apple_color[0], apple_color[1] - dg_apple, apple_color[2]]
        apple_color_field.setSFColor(apple_color)
        counter += 1


hand_reach_apple(1000)
hand_cut_apple(500)
