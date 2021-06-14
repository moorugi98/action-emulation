"""ButtonController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Display

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

bumper = robot.getDevice('touch sensor')
display = robot.getDevice('display')

bumper.enable(timestep)

red = 16711680
green = 65280
index = 0

display_on = False
switch_pressed = False
display.setColor(red)
display.fillRectangle(0,0,64,64)


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
  
   touch_value = bumper.getValue()
   #print(touch_value)
   
   if switch_pressed == False and touch_value == 1.0:
   
       if display_on == False:
           display.setColor(green)
           display.fillRectangle(0,0,64,64)
           display_on = True
           switch_pressed = True
           
           
       else:
       
           display.setColor(red)
           display.fillRectangle(0,0,64,64)
           display_on = False
           switch_pressed = True
           
           
   if touch_value == 0.0:
      
        switch_pressed = False
        
     
  
   
   
  
   
   pass

# Enter here exit cleanup code.
