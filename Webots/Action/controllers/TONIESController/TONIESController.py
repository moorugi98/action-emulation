"""TONIESController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Speaker
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
speaker = robot.getDevice('speaker')
bumper = robot.getDevice('touch sensor')
sound = ["robot_sound.wav", "robot_bip.wav"]
receiver = robot.getDevice('receiver')

bumper.enable(timestep)
receiver.enable(timestep)

#New figure on bumper?
change = True

while robot.step(timestep) != -1:
    # Read the sensors:
    touch_value = bumper.getValue()
  
        
    if touch_value == 1.0 and change:
       
        #check if anything is in queue:
        check = receiver.getQueueLength()
        if check > 0:
            change = False
            #receive message and unpack
            message = receiver.getData()
            info = struct.unpack('i', message)
            sound_index = info[0]
            speaker.playSound(speaker,speaker,sound[sound_index], 0.5, 1.0, 1.0, True)
            
        
    if touch_value == 0.0 and change == False:
         speaker.stop(sound[sound_index])
         change = True
         
    #get next package in queue (and delete head package)
    receiver.nextPacket()
  
    pass

# Enter here exit cleanup code.
