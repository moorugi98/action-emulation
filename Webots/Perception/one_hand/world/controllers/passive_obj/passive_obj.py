"""passive_obj controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Connector


# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# et the instance of a device
connector = robot.getDevice("connector")
connector.enablePresence(timestep)

while robot.step(timestep) != -1:
    print(connector.isLocked())
