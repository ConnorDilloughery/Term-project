"""!
@file main.py
Author: Connor Dilloughery

"""
import utime as time
import mlx_cam as Cam
from machine import Pin, I2C
from mlx90640 import RefreshRate

import gc
import pyb
import cotask
import task_share

import motorDriver as Vroom
import encoder
import MotorControl

#from motorstuff import *
gc.collect()

def main():
    
    state = 0
    middle = 0
    gc.collect()
    
    #camera = Cam.MLX_Cam(pyb.I2C (1, pyb.I2C.MASTER, baudrate = 100000), 29)
    #camera.active()
    
    
    try:
        from pyb import info

    # Oops, it's not an STM32; assume generic machine.I2C for ESP32 and others
    except ImportError:
        # For ESP32 38-pin cheapo board from NodeMCU, KeeYees, etc.
        i2c_bus = I2C(1, scl=Pin(22), sda=Pin(21))

    # OK, we do have an STM32, so just use the default pin assignments for I2C1
    else:
        i2c_bus = I2C(1)

    print("MXL90640 Easy(ish) Driver Test")
    gc.collect()
    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33
    scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
    print(f"I2C Scan: {scanhex}")
    
   # Cam.refresh_rate = RefreshRate.REFRESH_32_HZ
    
    gc.collect()
    # Create the camera object and set it up in default mode
    camera = Cam.MLX_Cam(i2c_bus)
    gc.collect()

    
    try:
        while True:
            if state == 0:
                # initialization
                # must wait for button to be pressed, set state = 1 when pressed
                print('state 0, initialization')
                state = 1
                time.sleep_ms(100)
            
            elif state == 1:
                # rotate motor
                print('state 1 Rotate the base')
                # check to see if position of base is complete
                state = 2
                time.sleep_ms(100)
                
            elif state == 2:
                print('state 2 - thermal state')
                tl = 0
                tm = 0
                tr = 0
                ml = 0
                m = 0
                mr = 0
                bl = 0
                bm = 0
                br = 0
                
                try:
                    # Get and image and see how long it takes to grab that image
                    print("Click.", end='')
                    begintime = time.ticks_ms()
                    image = camera.get_image()
                    print(f" {time.ticks_diff(time.ticks_ms(), begintime)} ms")

                    pixel_array = camera.get_array(image.pix)
                    
                    #print(pixel_array)
                    time.sleep_ms(1000)
                    gc.collect()

                except KeyboardInterrupt:
                    break
                max_val = max(pixel_array)
                print(max_val)
                index = 0
                #print(pixel_array)
                
                #print(len(pixel_array))
#                 for i in range(len(pixel_array)):
#                     if pixel_array[i] > max_val:
#                         max_val = pixel_array[i]
#                         index = i
                for i in pixel_array:
                    if i == max_val:
                        break
                    index += 1
                
                print(max_val, index)
                row = index // 32
                column = index % 32
                
                print(row, column)
                
                if row < 8:
                    if column < 11:
                        tl = 1
                        state = 3
                    elif column < 21:
                        tm = 1
                        state = 4
                    else:
                        tr = 1
                        state = 5
                elif row >= 8 and row < 16:
                    if column < 11:
                        ml = 1
                        state = 6
                    elif column < 21:
                        m = 1
                        state = 7
                    else:
                        mr = 1
                        state = 8
                else:
                    if column < 11:
                        bl = 1
                        state = 9
                    elif column < 21:
                        bm = 1
                        state = 10
                    else:
                        br = 1
                        state = 11    
                    time.sleep_ms(100)
                    
            elif state == 3:
                print('top left')
                # rotate base right
                # rotate down
                state = 2
                middle = 0
                Kp1 = 0.0012
                theta1 = 30000
                Kp2 = 0.0012
                theta2 = 30000
                run_motor(Kp1, theta1, Kp2, theta2)
                time.sleep_ms(100)
            elif state == 4:
                print('top middle')
                # rotate down
                state = 2
                middle = 0
                time.sleep_ms(100)
            elif state == 5:
                print('top right')
                # rotate base left
                # rotate down
                state = 2
                middle = 0
                time.sleep_ms(100)
            elif state == 6:
                print('middle left')
                # rotate base right
                
                state = 2
                middle = 0
                time.sleep_ms(100)
            elif state == 7:
                print('middle just perfect')
                middle += 1

                if middle == 2:
                    print('go time')
                    state = 12
                else:
                    state = 2  
                time.sleep_ms(100)
            elif state == 8:
                print('middle right')
                # rotate base left
                
                state = 2
                middle = 0
                time.sleep_ms(100)
            elif state == 9:
                print('bottom left')
                # rotate base right
                # rotate up
                state = 2
                middle = 0
                time.sleep_ms(100)
            elif state == 10:
                print('bottom mid')
                
                # rotate up
                state = 2
                middle = 0
                time.sleep_ms(100)
            elif state == 11:
                print('bottom right')
                # rotate base left
                # rotate up
                state = 2
                middle = 0
                time.sleep_ms(100)
            elif state == 12:
                print('Activating the gun')
                # Turn on the gun's motors
                state = 13
                time.sleep_ms(3000)
            elif state == 13:
                print('loading the gun--- FIRE!!!!')
                state = 14
                time.sleep_ms(3000)
            else:
                print('YAYUHH FIRE IN DA HOLE')
                # deactivate system
                break
        print ("Done.")
                
    except KeyboardInterrupt:
        print('Keyboard Interrupted')

def run_motor(Kp1, theta1, Kp2, theta2):
    #Createing the tasks that will be put into a scheduler. The period and priority of each
    #task is set.
    
    #task1 is responsible for the first motor of the two that are being controlled
    task1 = cotask.Task(task1_Motor, name="Task_1", priority=1, period=100,
                        profile=True, trace=False)
    #task2 is responsible for the second motor of the two that are being controlled
    task2 = cotask.Task(task2_Motor, name="Task_2", priority=1, period=100,
                       profile=True, trace=False)
    
    
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()
    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
            if task1_Motor() == 1 and task2_Motor() == 1:
                break
        except KeyboardInterrupt:
            break
    
def task1_Motor():#Kp1, theta1):
        '''!
        Task which controls the position of the first motor. There are no input parameters as the values chosen were selected withing
        the function itself
    
        '''
        don1 = 0
        #Initiating the communication interface through UART
        ser= pyb.UART(2,baudrate= 115200)
        #Specifying the motor shield EN pin
        EN_PIN= 'PC1'
        #Specifyinng the In1 pin for the motor shield
        IN1= 'PA0'
        #Specifying the IN2 pin for the motor shield
        IN2= 'PA1'
        #SPecifying the Timer 
        TIMER=5;
        #Specifying the first encoder input pin
        ENC1= 'PC6'
        #Specifying the second encoder input pin
        ENC2= 'PC7'
        #Specifying the encoder Timer
        ENCT= 8
        #Specifying the Theta value that is wanted
        Theta_Want= 100000#theta1
        #Specifying the value for Kp
        #Kp=10
        Kp= .0012#Kp1
        #Creating the motor object
        Motor1= Vroom.MotorDriver(EN_PIN, IN1, IN2, TIMER)
        #Creating the encoder object for the motor
        Motor1E= encoder.Encoder(ENC1, ENC2, ENCT)
        #Setting the motor to 0. Off
        Motor1.set_duty_cycle(0)
        
        while True:
            #Creating the motor proprtional control object
            Motor1PC= MotorControl.PropControl(Kp, Theta_Want)
            #Input command specifies if instruction has received of not
            Input_Command=0

            #Initiating the Position List
            #Position=[]
            #Initiating the Time List
            #Time=[]
            #Creating the TimeMs Variable to store the time
            TimeMs= 0
            #Setting the instance that the code began running
            TimeOld= time.ticks_ms()
            Theta_Count_Old = -1
            while True:
                  
                 #Reading the current position of the motor
                 Theta_Count= Motor1E.read()
                 delta_Theta = Theta_Count - Theta_Count_Old
                 #Calculating the new PWM value depending on the current position of the motor
                 PWM = Motor1PC.run( Theta_Count, Theta_Want)

                 Theta_Count_Old = Theta_Count
                 #Setting the PWM of the motor using the new value that was created
                 Motor1.set_duty_cycle(PWM)
                 #Receiving code was created to receive two different serial writes
                 #The count is sent first
                 #ser.write(f"CountOne: {Theta_Count}\r\n")
                 #Right after, the time in ms is sent
                 #ser.write(f"TimeOne: {TimeMs}\r\n")
                 #The tine difference in calculated and then added to the old value of TimeMs
                 TimeMs+= time.ticks_ms()-TimeOld
                 #print(TimeMs)
                 #TimeOld is specified as a new value
                 TimeOld= time.ticks_ms()
                 
                 if delta_Theta == 0:
                     print('here')
                     
                 #Position list gets appended with teh lated position value
                 #Position.append(Theta_Count)
                 #Time list gets appended with the latest time value
                 #Time.append(TimeMs)
                
                 
                 #print(PWM)
                 #print(Theta_Count, Theta_Want)
                 #if PWM <= 15:
                 # Needs a condition that 
                 #if Theta_Count >= Theta_Want:
                     #print('Time to leave')
                     #ser.write(f"Done\r\n")
                 #After 5 seconds, the program is to stop
                 #if TimeMs >= 5000:
                     #Sending Done to the host PC to signal that all teh data has been sent
                     #ser.write(f"Done\r\n")
                     #Stopping the loop once a data has been sent
                     done1 = 1
                     return done1
                 time.sleep_ms(6)
                     #break
                 yield 0
                 
            
            yield 0
            #while True:
                #Kp Value changed to a value that works with the period to avoid severe oscillation
             #   Motor1PC.set_Kp(.1)
                #Current position is being continuosly checked to keep motor in place
              #  Theta_Count= Motor1E.read()
                #The motor pwm is neing set to fix position if required
               # Motor1.set_duty_cycle(Motor1PC.run(Theta_Count, Theta_Want))
                #if Theta_Count >= Theta_Want:
                   # print('should stop')
                   # break
                
                #yield 0
            
        
    
    
def task2_Motor():#Kp2, theta2):
        """!
        Task which controls the position of the first motor. There are no input parameters as the values chosen were selected withing
        the function itself
        
        """
        done2 = 0
        #Initiating the communication interface through UART
        ser= pyb.UART(2,baudrate= 115200)
        #Specifying the motor shield EN pin
        EN_PIN= 'PA10'
        #Specifyinng the In1 pin for the motor shield
        IN1= 'PB4'
        #Specifying the IN2 pin for the motor shield
        IN2= 'PB5'
        #SPecifying the Timer 
        TIMER=3;
        #Specifying the first encoder input pin
        ENC2= 'PB6'
        #Specifying the second encoder input pin
        ENC1= 'PB7'
        #Specifying the encoder Timer
        ENCT= 4
        #Specifying the Theta value that is wanted
        Theta_Want2= -300000#theta2
        #Specifying the value for Kp
        #Kp=10
        Kp= 0.0012#Kp2
        #Creating the motor object
        Motor2= Vroom.MotorDriver(EN_PIN, IN1, IN2, TIMER)
        #Creating the encoder object for the motor
        Motor2E= encoder.Encoder(ENC1, ENC2, ENCT)
        #Setting the motor to 0. Off
        Motor2.set_duty_cycle(0)
        
        while True:
            #Creating the motor proprtional control object
            Motor2PC= MotorControl.PropControl(Kp, Theta_Want2)
            #Input command specifies if instruction has received of not
            Input_Command=0

            #Initiating the Position List
            #Position2=[]
            #Initiating the Time List
            #Time2=[]
            #Creating the TimeMs Variable to store the time
            TimeMs2= 0
            #Setting the instance that the code began running
            TimeOld2= time.ticks_ms()
            
            Theta_Count_Old2 = -1
            
            while True :
                  
     
                 #Reading the current position of the motor
                 Theta_Count2= Motor2E.read()
                 delta_Theta2 = Theta_Count2 - Theta_Count_Old2
                 if delta_Theta2 == 0:
                     print('dine')
                     done2 = 1
                     return done2
                     
                 Theta_Count_Old2 = Theta_Count2
                 #Calculating the new PWM value depending on the current position of the motor
                 PWM2 = Motor2PC.run( Theta_Count2, Theta_Want2)
                 #Setting the PWM of the motor using the new value that was created
                 Motor2.set_duty_cycle(PWM2)
                 #Receiving code was created to receive two different serial writes
                 #The count is sent first
                 #ser.write(f"CountTwo: {Theta_Count2}\r\n")
                 #Right after, the time in ms is sent
                 #ser.write(f"TimeTwo: {TimeMs2}\r\n")
                 #The tine difference in calculated and then added to the old value of TimeMs
                 TimeMs2+= time.ticks_ms()-TimeOld2
                 #print(TimeMs2)
                 #TimeOld is specified as a new value
                 TimeOld2= time.ticks_ms()
                 #Position list gets appended with teh lated position value
                 #Position2.append(Theta_Count2)
                 #Time list gets appended with the latest time value
                 #Time2.append(TimeMs2)
                
                 time.sleep_ms(6)
                 #print(PWM2)
                 #if PWM2 <= 13.05:
                 #if Theta_Count2 >= Theta_Want2:
                     #ser.write(f"Done\r\n")
                     
                     #print('time to leave')
                     
                     
                 #After 5 seconds, the program is to stop
                 #if TimeMs2 >= 5000:
                     #Sending Done to the host PC to signal that all teh data has been sent
                   #  ser.write(f"Done\r\n")
                     #Stopping the loop once a data has been sent
                     
                     #break
                 yield 0
                 
            yield 0
            
           # while True:
                #Setting Kp to a value that works with the period that the motor is running at
             #   Motor2PC.set_Kp(.1)
                #Constantly checking position to see if it has moved
              #  Theta_Count2= Motor2E.read()
                #Readjusting PWM to fix position
               # Motor2.set_duty_cycle(Motor2PC.run(Theta_Count2, Theta_Want2))
                #if theta_Count2 >= Theta_Want2:
                    #break
                
                #yield 0
            




if __name__ == "__main__":
    # check if button pressed here
    main()

        

