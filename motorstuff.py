"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.
@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share



import utime
import motorDriver as Vroom
import encoder
import MotorControl



def task1_Motor():
        '''!
        Task which controls the position of the first motor. There are no input parameters as the values chosen were selected withing
        the function itself
    
        '''
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
        Theta_Want= 100000
        #Specifying the value for Kp
        #Kp=10
        Kp= .012
        #Creating the motor object
        Motor1= Vroom.MotorDriver(EN_PIN, IN1, IN2, TIMER)
        #Creating the encoder object for the motor
        Motor1E= encoder.Encoder(ENC1, ENC2, ENCT)
        #Setting the motor to 0. Off
        Motor1.set_duty_cycle(0)
        gc.collect()
        while True:
            #Creating the motor proprtional control object
            Motor1PC= MotorControl.PropControl(Kp, Theta_Want)
            #Input command specifies if instruction has received of not
            Input_Command=0

            #Initiating the Position List
            Position=[]
            #Initiating the Time List
            Time=[]
            #Creating the TimeMs Variable to store the time
            TimeMs= 0
            #Setting the instance that the code began running
            TimeOld= utime.ticks_ms()
            while True:
                gc.collect()
                  
                  
                
     
                 #Reading the current position of the motor
                Theta_Count= Motor1E.read()
                 
                 
                 #Calculating the new PWM value depending on the current position of the motor
                PWM = Motor1PC.run( Theta_Count, Theta_Want)
                 #Setting the PWM of the motor using the new value that was created
                Motor1.set_duty_cycle(PWM)
                 #Receiving code was created to receive two different serial writes
                 #The count is sent first
                ser.write(f"CountOne: {Theta_Count}\r\n")
                 #Right after, the time in ms is sent
                ser.write(f"TimeOne: {TimeMs}\r\n")
                 #The tine difference in calculated and then added to the old value of TimeMs
                TimeMs+= utime.ticks_ms()-TimeOld
                print(TimeMs)
                 #TimeOld is specified as a new value
                TimeOld= utime.ticks_ms()
                 #Position list gets appended with teh lated position value
                Position.append(Theta_Count)
                 #Time list gets appended with the latest time value
                Time.append(TimeMs)
                
                 #utime.sleep_ms(6)
           
                 #After 5 seconds, the program is to stop
                if TimeMs >= 5000:
                     #Sending Done to the host PC to signal that all teh data has been sent
                    ser.write(f"Done\r\n")
                     #Stopping the loop once a data has been sent
                     
                    break
                yield 0
                 
            
            yield 0
            while True:
                #Kp Value changed to a value that works with the period to avoid severe oscillation
                Motor1PC.set_Kp(.1)
                #Current position is being continuosly checked to keep motor in place
                Theta_Count= Motor1E.read()
                #The motor pwm is neing set to fix position if required
                Motor1.set_duty_cycle(Motor1PC.run(Theta_Count, Theta_Want))
                
                yield 0
        
    
    
def task2_Motor():
        """!
        Task which controls the position of the first motor. There are no input parameters as the values chosen were selected withing
        the function itself
        
        """
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
        Theta_Want2= 150000
        #Specifying the value for Kp
        #Kp=10
        Kp2= .012
        #Creating the motor object
        Motor2= Vroom.MotorDriver(EN_PIN, IN1, IN2, TIMER)
        #Creating the encoder object for the motor
        Motor2E= encoder.Encoder(ENC1, ENC2, ENCT)
        #Setting the motor to 0. Off
        Motor2.set_duty_cycle(0)
        
        while True:
            #Creating the motor proprtional control object
            Motor2PC= MotorControl.PropControl(Kp2, Theta_Want2)
            #Input command specifies if instruction has received of not
            Input_Command=0

            #Initiating the Position List
            Position2=[]
            #Initiating the Time List
            Time2=[]
            #Creating the TimeMs Variable to store the time
            TimeMs2= 0
            #Setting the instance that the code began running
            TimeOld2= utime.ticks_ms()
            while True:
                  
                  
                
     
                 #Reading the current position of the motor
                 Theta_Count2= Motor2E.read()
                 
                 
                 #Calculating the new PWM value depending on the current position of the motor
                 PWM2 = Motor2PC.run( Theta_Count2, Theta_Want2)
                 #Setting the PWM of the motor using the new value that was created
                 Motor2.set_duty_cycle(PWM2)
                 #Receiving code was created to receive two different serial writes
                 #The count is sent first
                 ser.write(f"CountTwo: {Theta_Count2}\r\n")
                 #Right after, the time in ms is sent
                 ser.write(f"TimeTwo: {TimeMs2}\r\n")
                 #The tine difference in calculated and then added to the old value of TimeMs
                 TimeMs2+= utime.ticks_ms()-TimeOld2
                 print(TimeMs2)
                 #TimeOld is specified as a new value
                 TimeOld2= utime.ticks_ms()
                 #Position list gets appended with teh lated position value
                 Position2.append(Theta_Count2)
                 #Time list gets appended with the latest time value
                 Time2.append(TimeMs2)
                
                 #utime.sleep_ms(6)
           
                 #After 5 seconds, the program is to stop
                 if TimeMs2 >= 5000:
                     #Sending Done to the host PC to signal that all teh data has been sent
                     ser.write(f"Done\r\n")
                     #Stopping the loop once a data has been sent
                     
                     break
                 yield 0
                 
            
            yield 0
            
            while True:
                #Setting Kp to a value that works with the period that the motor is running at
                Motor2PC.set_Kp(.1)
                #Constantly checking position to see if it has moved
                Theta_Count2= Motor2E.read()
                #Readjusting PWM to fix position
                Motor2.set_duty_cycle(Motor2PC.run(Theta_Count2, Theta_Want2))
                
                yield 0
                
            


if __name__ == "__main__":

    #Createing the tasks that will be put into a scheduler. The period and priority of each
    #task is set.
    
    #task1 is responsible for the first motor of the two that are being controlled
    task1 = cotask.Task(task1_Motor, name="Task_1", priority=1, period=10,
                        profile=True, trace=False)
    #task2 is responsible for the second motor of the two that are being controlled
    task2 = cotask.Task(task2_Motor, name="Task_2", priority=1, period=10,
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
        except KeyboardInterrupt:
            break