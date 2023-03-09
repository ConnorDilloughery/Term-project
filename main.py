"""!
@file main.py
Author: Connor Dilloughery

"""
import utime as time
import mlx_cam as Cam
from machine import Pin, I2C
import gc
import pyb

def main():
    
    state = 0
    middle = 0
    
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

    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33
    scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
    print(f"I2C Scan: {scanhex}")
    
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

                # Can show image.v_ir, image.alpha, or image.buf; image.v_ir best?
                # Display pixellated grayscale or numbers in CSV format; the CSV
                # could also be written to a file. Spreadsheets, Matlab(tm), or
                # CPython can read CSV and make a decent false-color heat plot.
                
                try:
                    # Get and image and see how long it takes to grab that image
                    print("Click.", end='')
                    begintime = time.ticks_ms()
                    image = camera.get_image()
                    print(f" {time.ticks_diff(time.ticks_ms(), begintime)} ms")

                    # Can show image.v_ir, image.alpha, or image.buf; image.v_ir best?
                    # Display pixellated grayscale or numbers in CSV format; the CSV
                    # could also be written to a file. Spreadsheets, Matlab(tm), or
                    # CPython can read CSV and make a decent false-color heat plot.
                    pixel_array = camera.get_array(image.v_ir)
                    time.sleep_ms(1000)

                except KeyboardInterrupt:
                    break
                max_val = 0
                print(pixel_array)
                
                print(len(pixel_array))
                for i in range(1,len(pixel_array)):
                    if pixel_array[i] > max_val:
                        max_val = pixel_array[i]
                        index = i
                
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





if __name__ == "__main__":
    # check if button pressed here
    main()

        

