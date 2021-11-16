"""my_controller controller."""

# You may need to import some classes of the controller module.
import copy
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
init_hand_pos = [0.4, 0.3, -0.6]
init_red_pos = [0.4, 0.3, 0.55]
init_green_pos = [-0.35, 0.3, 0.4]
init_yellow_pos = [0.65, 0.3, -0.6]
init_hand_size = 0.5
big_hand_size = 1
small_hand_size = 0.25


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
pause(10)



# ### hand drops yellow
# print('hand drops yellow')
# openclose_step = 50
# pushpull_dist = 0.4

# #open hand
# ds = (big_hand_size - get_hand_size) / openclose_step
# counter = 0
# while (supervisor.step(timestep) != -1) and (counter < openclose_step):
    # get_hand_size += ds
    # get_field_hand_size.setSFFloat(get_hand_size)
    # counter += 1

# #close hand push
# ds = (get_hand_size - init_hand_size) / openclose_step
# dx = pushpull_dist * (get_yellow_pos[0] - get_hand_pos[0]) / openclose_step  # not vectorized cuz list needed
# dz = pushpull_dist * (get_yellow_pos[2] - get_hand_pos[2]) / openclose_step
# counter = 0
# while (supervisor.step(timestep) != -1) and (counter < openclose_step):
    # get_hand_size -= ds
    # get_field_hand_size.setSFFloat(get_hand_size)
    # get_yellow_pos[0] += dx
    # get_yellow_pos[2] += dz
    # get_field_yellow_pos.setSFVec3f(get_yellow_pos)
    # counter += 1
    
    

### hand grasps yellow
print('hand grasps yellow')
openclose_step = 50
pushpull_dist = 0.4
# #
#open hand
ds = (big_hand_size - get_hand_size) / openclose_step
counter = 0
while (supervisor.step(timestep) != -1) and (counter < openclose_step):
    get_hand_size += ds
    get_field_hand_size.setSFFloat(get_hand_size)
    counter += 1
# #
#close hand pull
ds = (get_hand_size - init_hand_size) / openclose_step
dx = pushpull_dist * (get_yellow_pos[0] - get_hand_pos[0]) / openclose_step  # not vectorized cuz list needed
dz = pushpull_dist * (get_yellow_pos[2] - get_hand_pos[2]) / openclose_step
counter = 0
while (supervisor.step(timestep) != -1) and (counter < openclose_step):
    get_hand_size -= ds
    get_field_hand_size.setSFFloat(get_hand_size)
    get_yellow_pos[0] -= dx
    get_yellow_pos[2] -= dz
    get_field_yellow_pos.setSFVec3f(get_yellow_pos)
    counter += 1








# ### hand transports yellow to red
# n_step = 120
# dz = 0.005
# dx = 0
# counter = 0
# while (supervisor.step(timestep) != -1) and (counter < n_step):

    # get_hand_pos = [get_hand_pos[0] + dx, get_hand_pos[1], get_hand_pos[2] + dz]
    # get_field_hand_pos.setSFVec3f(get_hand_pos)
    # get_yellow_pos = [get_yellow_pos[0] + dx, get_yellow_pos[1], get_yellow_pos[2] + dz]
    # get_field_yellow_pos.setSFVec3f(get_yellow_pos)
    # counter += 1
    
    
#
# pause(2000)
#
# n_step = 2000
# dz = 0
# dx = -0.0003
# counter = 0
# while (supervisor.step(timestep) != -1) and (counter < n_step):
    # get_red_pos = [get_red_pos[0] + dx, get_red_pos[1], get_red_pos[2] + dz]
    # get_field_red_pos.setSFVec3f(get_red_pos)
    # get_hand_pos = [get_hand_pos[0] + dx, get_hand_pos[1], get_hand_pos[2] + dz]
    # get_field_hand_pos.setSFVec3f(get_hand_pos)
    # counter += 1

# pause(2000)

# n_step = 1800
# dz = -0.0005
# dx = 0
# counter = 0
# while (supervisor.step(timestep) != -1) and (counter < n_step):
# get_hand_pos = [get_hand_pos[0] + dx, get_hand_pos[1], get_hand_pos[2] + dz]
# get_field_hand_pos.setSFVec3f(get_hand_pos)
# counter += 1
