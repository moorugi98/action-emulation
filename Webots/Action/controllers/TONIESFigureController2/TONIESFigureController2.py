"""TONIESFigureController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Emitter
from controller import Connector
import struct

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)
print("DOIFSDSOPFHDIP")
emitter2 = robot.getDevice("emitter")
connector_active = robot.getDevice("pc")
connector_active.enablePresence(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()
    info2 = struct.pack('i',1)
    emitter2.send(info2)
    #print("hello world")
    presence = connector_active.getPresence()
    if(presence == 1):
        connector_active.lock()    
    
   
    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
