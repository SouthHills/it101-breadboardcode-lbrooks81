# Description : Read Joystick state
from pathlib import Path
import sys
from gpiozero import Button
import time

HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import * 

USING_GRAVITECH_ADC = False # Only modify this if you are using a Gravitech ADC
    
BUTTON = Button(18) # define Z Pin (button)
ADC = ADCDevice() # Define an ADCDevice class object
last_direction = "Neutral"

def setup():
    global ADC
    if(ADC.detectI2C(0x48) and USING_GRAVITECH_ADC): 
        ADC = GravitechADC()
    elif(ADC.detectI2C(0x48)): # Detect the pcf8591.
        ADC = PCF8591()
    elif(ADC.detectI2C(0x4b)): # Detect the ads7830
        ADC = ADS7830()
    else:
        print("No correct I2C address found, \n"
            "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
            "Program Exit. \n")
        exit(-1)

def loop():
    global ADC, BUTTON
    while True:     
        val_Z = BUTTON.is_active # read digital value of axis Z
        val_Y = ADC.analogRead(0)           # read analog value of axis X and Y
        val_X = ADC.analogRead(1)
        print (f'Direction: {get_direction(val_X, val_Y)} \tvalue_X: {val_X} \tvlue_Y: {val_Y}\tvalue_Z: {val_Z}')
        time.sleep(0.01)
        
def get_direction(x, y):
    global last_direction
    DEAD_ZONE_RANGE = (100, 152)
    x_dead: bool = False
    y_dead: bool = False
    
    if (x == 0 and y == 0) or (x == 255 or y == 255):
        return last_direction
    
    if DEAD_ZONE_RANGE[0] <= x <= DEAD_ZONE_RANGE[1]:
        x_dead = True
        
    if DEAD_ZONE_RANGE[0] <= y <= DEAD_ZONE_RANGE[1]:
        y_dead = True
        
    if x_dead and y_dead:
        last_direction = 'Neutral'
    elif x_dead:
        last_direction = 'Up' if y < 127 else 'Down'
    elif y_dead:
        last_direction = 'Left' if x < 127 else 'Right'
    elif abs(127 - x) > abs(127 - y):
        last_direction = 'Left' if x < 127 else 'Right'
    elif abs(127 - y) > abs(127 - x):
        last_direction = 'Up' if y < 127 else 'Down'
     
    return last_direction

def destroy():
    global ADC, BUTTON
    ADC.close()
    BUTTON.close()
    
if __name__ == '__main__':
    print ('Program is starting ... ') # Program entrance
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
