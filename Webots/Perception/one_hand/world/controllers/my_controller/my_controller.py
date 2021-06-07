"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Supervisor, Keyboard, Connector

# get the supervisor which is +alpha on the default Robot()
supervisor = Supervisor()
# get the keyboard
keyboard = Keyboard()
# get the active connector on the hand
connector = Connector("hand_connector")
# get the time step of the current world.
timestep = int(supervisor.getBasicTimeStep())

# init stuff
connector.enablePresence(timestep)
keyboard.enable(timestep)
robot_node = supervisor.getSelf()
trans_field = robot_node.getField("translation")

# Inform user about control
print()

# Main loop
while supervisor.step(timestep) != -1:
    # Get position
    values = trans_field.getSFVec3f()

    # Get keyboard input
    key = keyboard.getKey()
    dx = 0.01
    if key == ord('D'):
        trans_field.setSFVec3f([values[0] + dx, values[1], values[2]])
    elif key == ord('A'):
        trans_field.setSFVec3f([values[0] - dx, values[1], values[2]])
    elif key == ord('S'):
        trans_field.setSFVec3f([values[0], values[1], values[2] + dx])
    elif key == ord('W'):
        trans_field.setSFVec3f([values[0], values[1], values[2] - dx])
    elif key == ord('R'):
        trans_field.setSFVec3f([values[0], values[1] + dx, values[2]])
    elif key == ord('F'):
        trans_field.setSFVec3f([values[0], values[1] - dx, values[2]])
    elif key == ord('Q'):  # set to initial pos
        trans_field.setSFVec3f([0, 1, 0])
    elif key == ord('E'): # enable or disable magnetic link
        if connector.isLocked():
            connector.unlock()
            print('magnet disabled')
        else:
            connector.lock()
            print('magnet enabled')
    
    # if the object is grabbed, indicate this by color change of hand
    # print(supervisor.getFromDef("hand_col").getField("baseColor").setSFColor([0,0,0]))

     



