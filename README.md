# Term Project Overview
Names: Connor Dilloughery, Erik Torres - Mech Tub 16

## Introduction
The purpose of this project is to create an automatic nerf gun that is fully self-automated. We created this device as apart of our ME 405 Term Project, 
which consists of code we've written over the quarter. This design is intended for anyone who likes to channel their inner-child self and want to blast 
someone which nerf darts without pulling a trigger. Our design consists of four motors, a themal camera, and a solenoid. We controlled two of the motors 
apart of this design in order to provide a yaw and a pitch rotation. The other two motors are apart of a nerf gun kit that accelerate two flywheels that 
provides the force to launch the darts. We also used a thermal camera so that the system could recognize where someone is based on the hightest temperature 
readings. Within our thermal system design, we are setting the yaw and pitch to a desired angle to position the gun in the direction of the person. In 
order to load a dart into the gun, we used a solenoid that pushes the darts in the spinning flywheels. To make the project more fun, we decided to make 
our gun fully automatic, launching 15 darts within 2 seconds by retracting and pushing the solenoid fifteen times.

## Hardware Overview
The hardware on apart of the design are as listed:
  - Nucleo STM 32L476
  - X-Nucleo-IHM04A1 Motor Driver
  - MLX 90640 
  - Metek motors (2)
  - Worker motors (2) 
  - Solenoid
 
As mentioned before, we only had to parameterize the Metek motors because controlling the motor position and speed was necessary. Using the MLX camera, the output from the device was split into a 3x3 grid to help center the camera at the location with the highest heat density. Two Metek motors were used to operate teh pitch and yaw of the system. Given that there were 5 seconds form the initial turn on period, a more accurate positioning system was opted for instead of doing a fast system. The gear ratio that was chosen on the project was a 16:1 gear ratio for both the yaw and the pitch. Combined with the gear ratio already installed internally within the motor, the final drive ratio was 256:1. This large gear reduction allowed for a full cycle to have an encoder count of about 200,000 ticks. This larger accuracy and slower travel was deemed as the better approach as it would allow for less overshoot and allow for the system to stop travel midway through after having received a new frame. With the opponent having to stop at the end, speed was not a priority throughout the concept of this device. 
Once the Metek motors aligned the turret with the target, the hardware associated with the shooting  mechanism was triggered. A pair of 132 motors by Worker were fitted into an aluminum flywheel cage with canted flywheels, which was also produced by worker. Upon finishing ramp up, a 12v solenoid is able to rapidly actuate to deliver the darts to the flywheels. 

### Full Design 
![image](https://user-images.githubusercontent.com/122577773/226222147-2c329de2-7c2a-43a1-b06c-6d770caa4d86.png)
![image](https://user-images.githubusercontent.com/122577773/226222177-a3a2ce05-a930-434d-a38e-5b1ee39daafd.png)


### Gear System Overview
#### Yaw Drive System 

## Software Overview
In make our software, we imported the following code: 
  - motorDriver.py
  - encoder.py
  - MotorControl.py
  - mlx_cam.py 
  - calibration.py
  - image.py
  - regmap.py
  - utilts.py
  - __init__.py
 
 In our main file, we used four different functions:
  - main(): This function includes all of the finite states and calls neccessary functions to run our hardware. 
  - task1_Motor(): This function is called when the yaw motor is required to move to a new position. It checks to see if the encoder value is
    near the desired position.
  - task2_Motor(): Performs the same task as task1_Motor(), but is used for the pitch motor. 
  - fire(): The fire function gets called when it's time to turn on the gun motors and activate the solenoid. It cycles through, turning the solenoid 
    off and on. 
    
 To make our thermal camera funcitonal for our code, we created a 3x3 matrix with the following purpose:
  - Top Left
  - Top Middle
  - Top Right 
  - Middle Left
  - Middle (Perfect)
  - Middle Right
  - Bottom Left
  - Bottom Middle
  - Bottom Right

When the thermal camera produced temperature readings, we cycled through the array looking for the largest value and its index. We used the index to determine the matrix position, which would give desired encoder postions to send to the motor function. 

To make our motors functional, we inputted a desired encoder positon value. We also assigned a proportional constant on the motor to tell our motor how fast to run. We used our code from Lab 2 to drive our motor. 
    
 The link to find these functions are: ____________________________________________
 
 Although the mechanical design did not work in the end, we were able to get the positional motors, thermal camera, gun, and solenoid working. As apart 
 of our demonstration, we should off the fully automatic setting of our gun. 
 
 To test our model, we first tested the thermal camera. We had one member hold up the thermal camera while the other stood ~10 feet away. We oriented 
 the camera to see it the member was being read by the camera. 
 
