"""my_controller controller."""

# You may need to import some classes of the controller module.
import copy
import math
from controller import Supervisor

# get the supervisor which is +alpha on the default Robot() allowing me to do whatever I like
supervisor = Supervisor()
# get the time step of the current world
timestep = int(supervisor.getBasicTimeStep())

# grab handles
get_field_hand_pos = supervisor.getSelf().getField('translation')
get_field_red_pos = supervisor.getFromDef('red').getField('translation')
get_field_green_pos = supervisor.getFromDef('green').getField('translation')
get_field_yellow_pos = supervisor.getFromDef('yellow').getField('translation')
get_hand_pos = get_field_hand_pos.getSFVec3f()
get_red_pos = get_field_red_pos.getSFVec3f()
get_green_pos = get_field_green_pos.getSFVec3f()
get_yellow_pos = get_field_yellow_pos.getSFVec3f()
get_freespace0_pos = [-0.6, 0.2, 0.5]
get_freespace1_pos = [0.7, 0.2, 0.5]

get_field_hand_size = supervisor.getFromDef("hand_geom").getField("radius")
get_hand_size = get_field_hand_size.getSFFloat()

# starting values
# diam. of a ball is 0.1, meaning 0.1 distance is just touching
# use 0.15 for close, 0.3 for far distance
init_hand_pos = [0.4, 0.3, -0.6]
init_red_pos = [0.4, 0.3, 0.4] 
init_green_pos = [-0.35, 0.3, 0.2]
init_yellow_pos = [0.25, 0.3, -0.6]  
init_hand_size = 0.5
big_hand_size = 1


def pause(n_step=200):
    counter = 0
    while (supervisor.step(timestep) != -1) and (counter < n_step):
        counter += 1


def reset():
    print("reset the simulation to initial condition")
    # set back to initial pos
    global get_hand_pos
    global get_red_pos
    global get_green_pos
    global get_yellow_pos
    get_hand_pos = init_hand_pos
    get_red_pos = init_red_pos
    get_green_pos = init_green_pos
    get_yellow_pos = init_yellow_pos
    get_field_hand_pos.setSFVec3f(get_hand_pos)
    get_field_red_pos.setSFVec3f(get_red_pos)
    get_field_green_pos.setSFVec3f(get_green_pos)
    get_field_yellow_pos.setSFVec3f(get_yellow_pos)

    # set to initial size
    global get_hand_size
    get_hand_size = init_hand_size
    get_field_hand_size.setSFFloat(get_hand_size)


reset()
pause(20)

    

grasp = False
### hand drops/grasps yellow
if grasp:
    print('hand grasps yellow')
else:
    print('hand drops yellow')
    
openclose_step = 50
pushpull_dist = 0.15  # 0.1 would be diameter of a ball
# #
# open hand
ds = (big_hand_size - get_hand_size) / openclose_step
counter = 0
while (supervisor.step(timestep) != -1) and (counter < openclose_step):
    get_hand_size += ds
    get_field_hand_size.setSFFloat(get_hand_size)
    counter += 1
# #
# close hand pull
ds = (get_hand_size - init_hand_size) / openclose_step
cur_x = (get_yellow_pos[0] - get_hand_pos[0])
cur_z = (get_yellow_pos[2] - get_hand_pos[2])
cur_hypote = math.sqrt(cur_x**2 + cur_z**2) # Pytagoras
dx = cur_x * pushpull_dist / cur_hypote / openclose_step
dz = cur_z * pushpull_dist / cur_hypote / openclose_step
if not grasp:
    dx = -1 * dx
    dz = -1 * dz
print(cur_x, cur_z, cur_hypote, dx, dz)
counter = 0
while (supervisor.step(timestep) != -1) and (counter < openclose_step):
    get_hand_size -= ds
    get_field_hand_size.setSFFloat(get_hand_size)
    get_yellow_pos[0] -= dx
    get_yellow_pos[2] -= dz
    get_field_yellow_pos.setSFVec3f(get_yellow_pos)
    counter += 1



pause(100)



### hand transports yellow to red
n_step = 140
dz = 0.005
dx = 0
counter = 0
while (supervisor.step(timestep) != -1) and (counter < n_step):

    get_hand_pos = [get_hand_pos[0] + dx, get_hand_pos[1], get_hand_pos[2] + dz]
    get_field_hand_pos.setSFVec3f(get_hand_pos)
    # get_yellow_pos = [get_yellow_pos[0] + dx, get_yellow_pos[1], get_yellow_pos[2] + dz]
    # get_field_yellow_pos.setSFVec3f(get_yellow_pos)
    counter += 1
    


pause(100)



grasp = True
### hand drops/grasps red
if grasp:
    print('hand grasps yellow')
else:
    print('hand drops yellow')
    
openclose_step = 50
pushpull_dist = 0.15  # 0.1 would be diameter of a ball
# #
# open hand
ds = (big_hand_size - get_hand_size) / openclose_step
counter = 0
while (supervisor.step(timestep) != -1) and (counter < openclose_step):
    get_hand_size += ds
    get_field_hand_size.setSFFloat(get_hand_size)
    counter += 1
# #
# close hand pull
ds = (get_hand_size - init_hand_size) / openclose_step
cur_x = (get_red_pos[0] - get_hand_pos[0])
cur_z = (get_red_pos[2] - get_hand_pos[2])
cur_hypote = math.sqrt(cur_x**2 + cur_z**2) # Pytagoras
dx = cur_x * pushpull_dist / cur_hypote / openclose_step
dz = cur_z * pushpull_dist / cur_hypote / openclose_step
if not grasp:
    dx = -1 * dx
    dz = -1 * dz
print(cur_x, cur_z, cur_hypote, dx, dz)
counter = 0
while (supervisor.step(timestep) != -1) and (counter < openclose_step):
    get_hand_size -= ds
    get_field_hand_size.setSFFloat(get_hand_size)
    get_red_pos[0] -= dx
    get_red_pos[2] -= dz
    get_field_red_pos.setSFVec3f(get_red_pos)
    counter += 1
    
    
    
pause(100)

    
    
### hand transports red to green
n_step = 110
dz = 0
dx = -0.005
counter = 0
while (supervisor.step(timestep) != -1) and (counter < n_step):

    get_hand_pos = [get_hand_pos[0] + dx, get_hand_pos[1], get_hand_pos[2] + dz]
    get_field_hand_pos.setSFVec3f(get_hand_pos)
    get_red_pos = [get_red_pos[0] + dx, get_red_pos[1], get_red_pos[2] + dz]
    get_field_red_pos.setSFVec3f(get_red_pos)
    counter += 1