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

# def main():
#     
#     state = 0
#     middle = 0
#     gc.collect()
#     
#     #camera = Cam.MLX_Cam(pyb.I2C (1, pyb.I2C.MASTER, baudrate = 100000), 29)
#     #camera.active()
#     
#     
# #     try:
# #         from pyb import info
# # 
# #     # Oops, it's not an STM32; assume generic machine.I2C for ESP32 and others
# #     except ImportError:
# #         # For ESP32 38-pin cheapo board from NodeMCU, KeeYees, etc.
# #         i2c_bus = I2C(1, scl=Pin(22), sda=Pin(21))
# # 
# #     # OK, we do have an STM32, so just use the default pin assignments for I2C1
# #     else:
# #         i2c_bus = I2C(1)
# # 
# #     print("MXL90640 Easy(ish) Driver Test")
# #     gc.collect()
# #     # Select MLX90640 camera I2C address, normally 0x33, and check the bus
# #     i2c_address = 0x33
# #     scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
# #     print(f"I2C Scan: {scanhex}")
# #     
# #    # Cam.refresh_rate = RefreshRate.REFRESH_32_HZ
# #     
# #     gc.collect()
# #     # Create the camera object and set it up in default mode
# #     camera = Cam.MLX_Cam(i2c_bus)
# #     gc.collect()
# 
#     
#     try:
#         while True:
#             if state == 0:
#                 # initialization
#                 # must wait for button to be pressed, set state = 1 when pressed
#                 print('state 0, initialization')
#                 state = 1
#                 time.sleep_ms(100)
#             
#             elif state == 1:
#                 # rotate motor
#                 print('state 1 Rotate the base')
#                 # check to see if position of base is complete
#                 state = 2
#                 time.sleep_ms(100)
#                 
#             elif state == 2:
#                 print('state 2 - thermal state')
#                 tl = 0
#                 tm = 0
#                 tr = 0
#                 ml = 0
#                 m = 0
#                 mr = 0
#                 bl = 0
#                 bm = 0
#                 br = 0
# #                 
# #                 try:
# #                     # Get and image and see how long it takes to grab that image
# #                     print("Click.", end='')
# #                     begintime = time.ticks_ms()
# #                     image = camera.get_image()
# #                     print(f" {time.ticks_diff(time.ticks_ms(), begintime)} ms")
# # 
# #                     pixel_array = camera.get_array(image.pix)
# #                     
# #                     #print(pixel_array)
# #                     time.sleep_ms(1000)
# #                     gc.collect()
# # 
# #                 except KeyboardInterrupt:
# #                     break
# #                 max_val = max(pixel_array)
# #                 print(max_val)
# #                 index = 0
# #                 #print(pixel_array)
# #                 
# #                 #print(len(pixel_array))
# # #                 for i in range(len(pixel_array)):
# # #                     if pixel_array[i] > max_val:
# # #                         max_val = pixel_array[i]
# # #                         index = i
# #                 for i in pixel_array:
# #                     if i == max_val:
# #                         break
# #                     index += 1
# #                 
# #                 print(max_val, index)
# #                 row = index // 32
# #                 column = index % 32
# #                 
# #                 print(row, column)
#                 
# #                 if row < 8:
# #                     if column < 11:
# #                         tl = 1
# #                         state = 3
# #                     elif column < 21:
# #                         tm = 1
# #                         state = 4
# #                     else:
# #                         tr = 1
# #                         state = 5
# #                 elif row >= 8 and row < 16:
# #                     if column < 11:
# #                         ml = 1
# #                         state = 6
# #                     elif column < 21:
# #                         m = 1
# #                         state = 7
# #                     else:
# #                         mr = 1
# #                         state = 8
# #                 else:
# #                     if column < 11:
# #                         bl = 1
# #                         state = 9
# #                     elif column < 21:
# #                         bm = 1
# #                         state = 10
# #                     else:
# #                         br = 1
# #                         state = 11    
# #                     time.sleep_ms(100)
#                     
#             elif state == 3:
#                 print('top left')
#                 # rotate base right
#                 # rotate down
#                 state = 2
#                 middle = 0
#                 Kp1 = 0.0012
#                 theta1 = 30000
#                 Kp2 = 0.0012
#                 theta2 = 30000
#                 run_motor(Kp1, theta1, Kp2, theta2)
#                 time.sleep_ms(100)
#             elif state == 4:
#                 print('top middle')
#                 # rotate down
#                 state = 2
#                 middle = 0
#                 time.sleep_ms(100)
#             elif state == 5:
#                 print('top right')
#                 # rotate base left
#                 # rotate down
#                 state = 2
#                 middle = 0
#                 time.sleep_ms(100)
#             elif state == 6:
#                 print('middle left')
#                 # rotate base right
#                 
#                 state = 2
#                 middle = 0
#                 time.sleep_ms(100)
#             elif state == 7:
#                 print('middle just perfect')
#                 middle += 1
# 
#                 if middle == 2:
#                     print('go time')
#                     state = 12
#                 else:
#                     state = 2  
#                 time.sleep_ms(100)
#             elif state == 8:
#                 print('middle right')
#                 # rotate base left
#                 
#                 state = 2
#                 middle = 0
#                 time.sleep_ms(100)
#             elif state == 9:
#                 print('bottom left')
#                 # rotate base right
#                 # rotate up
#                 state = 2
#                 middle = 0
#                 time.sleep_ms(100)
#             elif state == 10:
#                 print('bottom mid')
#                 
#                 # rotate up
#                 state = 2
#                 middle = 0
#                 time.sleep_ms(100)
#             elif state == 11:
#                 print('bottom right')
#                 # rotate base left
#                 # rotate up
#                 state = 2
#                 middle = 0
#                 time.sleep_ms(100)
#             elif state == 12:
#                 print('Activating the gun')
#                 # Turn on the gun's motors
#                 state = 13
#                 time.sleep_ms(3000)
#             elif state == 13:
#                 print('loading the gun--- FIRE!!!!')
#                 state = 14
#                 time.sleep_ms(3000)
#             else:
#                 print('YAYUHH FIRE IN DA HOLE')
#                 # deactivate system
#                 break
#         print ("Done.")
#                 
#     except KeyboardInterrupt:
#         print('Keyboard Interrupted')

def run_project():
    #Createing the tasks that will be put into a scheduler. The period and priority of each
    #task is set.
    thermal_time = task_share.Share('B', thread_protect=False, name="Thermal Position")
    theta_want1 = task_share.Queue('l', 16, thread_protect=False, overwrite=False,
                          name="theta1_want1")
    theta_want2 = task_share.Queue('l', 16, thread_protect=False, overwrite=False,
                          name="theta1_want2")
    fire_time = task_share.Queue('B', 16, thread_protect=False, name="theta1_want1")
    
    #task1 is responsible for the first motor of the two that are being controlled
    task1 = cotask.Task(task1_Motor, name="Task_1_Motor_1", priority=1, period=150,
                       profile=True, trace=False, shares=(thermal_time, theta_want1, theta_want2, fire_time))
    #task2 is responsible for the second motor of the two that are being controlled
    task2 = cotask.Task(task2_Motor, name="Task_2_Motor_2", priority=1, period=150,
                       profile=True, trace=False, shares=(thermal_time, theta_want1, theta_want2, fire_time))
    
    task3 = cotask.Task(task3_Thermal, name="Task_3_Thermal", priority=2, period=800,
                       profile=True, trace=False, shares=(thermal_time, theta_want1, theta_want2, fire_time))
    
    task4 = cotask.Task(task4_Fire, name= "Task_4", priority=2, period= 1500,
                       profile=True, trace=False, shares=(thermal_time, theta_want1, theta_want2, fire_time))
    
    
    
    
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)
    cotask.task_list.append(task4)
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()
    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    count = 0
    thermal_time.put(0)
    theta_want1.put(300000)
    theta_want2.put(0)
    fire_time.put(0)
    #print(thermal_time.get())
    #print(str(thermal_time))
               
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')
        

            
    
def task1_Motor(shares):#Kp1, theta1):
        '''!
        Task which controls the position of the first motor. There are no input parameters as the values chosen were selected withing
        the function itself
    
        '''
        thermal_time, theta_want1, theta_want2, fire_time = shares
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
        Theta_Want = theta_want1.get()#theta1
        #print(Theta_Want)
        #Specifying the value for Kp
        #Kp=10
        Kp= .0012#Kp1
        #Creating the motor object
        Motor1= Vroom.MotorDriver(EN_PIN, IN1, IN2, TIMER)
        #Creating the encoder object for the motor
        Motor1E= encoder.Encoder(ENC1, ENC2, ENCT)
        #Setting the motor to 0. Off
        Motor1.set_duty_cycle(0)
        Theta_Count_Old = -1 # want nonzero value to prevent delta_theta from being 0 at the start
        counter = 0
        while True:
            while theta_want1.any():
                
                #Reading the current position of the motor
                Theta_Count = Motor1E.read()
                #delta_Theta2 = Theta_Count2 - Theta_Count_Old2
                if abs(Theta_Count - Theta_Count_Old) > 1000 or counter < 1000 :
                    #Calculating the new PWM value depending on the current position of the motor
                    PWM = Motor1PC.run(Theta_Count, Theta_Want)
                    Motor1.set_duty_cycle(PWM)
                    Theta_Count_Old = Theta_Count
                    
                else:
                    PWM = 0
                    Motor1.set_duty_cycle(PWM)
                    #break
                    yield 0
                counter += 1
            while True:
                
                #print('1')
                PWM = 0
                Motor1.set_duty_cycle(PWM)
                thermal_time.put(1)
                theta_want1.put(0)
                theta_want2.put(0)
                fire_time.put(0)
                    #yield 0
               
                

            Theta_Count_Old2 = Theta_Count2
            time.sleep_ms(6)
                #break
            yield 0
             
        
        yield 0
            
        
    
    
def task2_Motor(shares):#Kp2, theta2):
        """!
        Task which controls the position of the first motor. There are no input parameters as the values chosen were selected withing
        the function itself
        
        """
        thermal_time, theta_want1, theta_want2, fire_time = shares
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
        Theta_Want2= theta_want2.get()#theta2
        #Specifying the value for Kp
        #Kp=10
        Kp= 0.0012#Kp2
        #Creating the motor object
        Motor2= Vroom.MotorDriver(EN_PIN, IN1, IN2, TIMER)
        #Creating the encoder object for the motor
        Motor2E= encoder.Encoder(ENC1, ENC2, ENCT)
        #Setting the motor to 0. Off
        Motor2.set_duty_cycle(0)
        print(thermal_time)
        Theta_Count_Old2 = -1 # want nonzero value to prevent delta_theta from being 0 at the start
        while True:
            while theta_want2.any():
                      
                #Reading the current position of the motor
                Theta_Count2 = Motor2E.read()
                #delta_Theta2 = Theta_Count2 - Theta_Count_Old2
                if abs(Theta_Count2 - Theta_Count_Old2) > 1000 :
                    #Calculating the new PWM value depending on the current position of the motor
                    PWM2 = Motor2PC.run(Theta_Count2, Theta_Want2)
                    Motor2.set_duty_cycle(PWM2)
                    Theta_Count_Old2 = Theta_Count2
                    
                else:
                    PWM2 = 0
                    Motor2.set_duty_cycle(PWM2)
                    break
                    #yield 0
            while True:
                
                #print('1')
                PWM2 = 0
                Motor2.set_duty_cycle(PWM2)
                thermal_time.put(1)
                theta_want1.put(0)
                theta_want2.put(0)
                fire_time.put(0)
                    #yield 0
               
                

            Theta_Count_Old2 = Theta_Count2
            time.sleep_ms(6)
                #break
            yield 0
             
        
        yield 0

               
               
def task3_Thermal(shares):
    thermal_time, theta_want1, theta_want2, fire_time = shares
    print('ererer')
    try:
        from pyb import info

    # Oops, it's not an STM32; assume generic machine.I2C for ESP32 and others
    except ImportError:
        # For ESP32 38-pin cheapo board from NodeMCU, KeeYees, etc.
        i2c_bus = I2C(1, scl=Pin(22), sda=Pin(21))

    # OK, we do have an STM32, so just use the default pin assignments for I2C1
    else:
        i2c_bus = I2C(1)
    while True:
        #print('here now')
        while thermal_time.get():
            print('down here')
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
                # Get and image and see how long it takes to grab that image
                print("Click.", end='')
                begintime = time.ticks_ms()
                image = camera.get_image()
                print(f" {time.ticks_diff(time.ticks_ms(), begintime)} ms")

                pixel_array = camera.get_array(image.pix)
                
                #print(pixel_array)
                #time.sleep_ms(1000)
                gc.collect()
                max_val = max(pixel_array)
                print(max_val)
                index = 0
                max_index = 0
                #print(pixel_array)
                
                #print(len(pixel_array))
#                 for i in range(len(pixel_array)):
#                     if pixel_array[i] > max_val:
#                         max_val = pixel_array[i]
#                         index = i
                for i in pixel_array:
                    if i == max_val:
                        max_index = index
                    index += 1
                
                print(max_val, index)
                row = index // 32
                column = index % 32
                
                print(row, column)
                if row < 8:
                    if column < 11:

                        thermal_time.put(0)
                        theta_want1.put(10000)
                        theta_want2.put(-10000)
                        fire_time.put(0)
                    elif column < 21:
                        tm = 1
                        state = 4
                        thermal_time.put(0)
                        theta_want1.put(0)
                        theta_want2.put(-10000)
                        fire_time.put(0)
                    else:

                        thermal_time.put(0)
                        theta_want1.put(-10000)
                        theta_want2.put(-10000)
                        fire_time.put(0)
                elif row >= 8 and row < 16:
                    if column < 11:

                        thermal_time.put(0)
                        theta_want1.put(10000)
                        theta_want2.put(0)
                        fire_time.put(0)
                    elif column < 21:

                        thermal_time.put(0)
                        theta_want1.put(0)
                        theta_want2.put(0)
                        fire_time.put(1)
                    else:

                        thermal_time.put(0)
                        theta_want1.put(-10000)
                        theta_want2.put(0)
                        fire_time.put(0)
                else:
                    if column < 11:

                        thermal_time.put(0)
                        theta_want1.put(10000)
                        theta_want2.put(10000)
                        fire_time.put(0)
                    elif column < 21:

                        thermal_time.put(0)
                        theta_want1.put(0)
                        theta_want2.put(10000)
                        fire_time.put(0)
                    else:

                        thermal_time.put(0)
                        theta_want1.put(-10000)
                        theta_want2.put(10000)
                        fire_time.put(0)
                    time.sleep_ms(100)
                

            except KeyboardInterrupt:
                break
            
            yield 0
    
        while True:
            
            yield 0
        
def task4_Fire(shares):
    thermal_time, theta_want1, theta_want2, fire_time = shares
    pass
#     while True:
#         pass
#         if fire_time == 1:
#             print('here')
#             
#             
#             thermal_time.put(0)
#             theta_want1.put(0)
#             theta_want2.put(0)
#             fire_time.put(1)
#         else:
#             thermal_time.put(1)
#             
#             
#     pass




if __name__ == "__main__":
    # check if button pressed here
    run_project()

        

