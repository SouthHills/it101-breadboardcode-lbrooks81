# Description : Read Joystick state
from pathlib import Path
import sys
from gpiozero import Button

HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import * 

class Joystick:
    USING_GRAVITECH_ADC = False # Only modify this if you are using a Gravitech ADC
        
    BUTTON = Button(18) # define Z Pin (button)
    ADC = ADCDevice() # Define an ADCDevice class object
    last_direction = "Neutral"
    button_pressed_momentary = False

    def __init__(self):
        if(self.ADC.detectI2C(0x48) and self.USING_GRAVITECH_ADC): 
            self.ADC = GravitechADC()
        elif(self.ADC.detectI2C(0x48)): # Detect the pcf8591.
            self.ADC = PCF8591()
        elif(self.ADC.detectI2C(0x4b)): # Detect the ads7830
            self.ADC = ADS7830()
        else:
            print("No correct I2C address found, \n"
                "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
                "Program Exit. \n")
            exit(-1)

    def get_xy_pos(self):   
        val_Z = self.BUTTON.is_active # read digital value of axis Z
        val_Y = self.ADC.analogRead(0)           # read analog value of axis X and Y
        val_X = self.ADC.analogRead(1)
        return self.get_direction(val_X, val_Y), val_X, val_Y, val_Z
    
    def get_button_pressed(self):
        button_pressed = self.BUTTON.is_active
        if button_pressed and not self.button_pressed_momentary:
            self.button_pressed_momentary = True
        else:
            self.button_pressed_momentary = False
        return self.button_pressed_momentary
            
    def get_direction(self, x = None, y = None):
        # If this method has been called seperately from get_xy_pos(), x and y need values
        if x == None or y == None:
            x = self.ADC.analogRead(1)           # read analog value of axis X and Y
            y = self.ADC.analogRead(0)
        
        DEAD_ZONE_RANGE = (100, 152)
        x_dead: bool = False
        y_dead: bool = False
        
        if (x == 0 and y == 0) or (x == 255 or y == 255):
            return self.last_direction
        
        if DEAD_ZONE_RANGE[0] <= x <= DEAD_ZONE_RANGE[1]:
            x_dead = True
            
        if DEAD_ZONE_RANGE[0] <= y <= DEAD_ZONE_RANGE[1]:
            y_dead = True
            
        if x_dead and y_dead:
            self.last_direction = 'Neutral'
        elif x_dead:
            self.last_direction = 'Up' if y < 127 else 'Down'
        elif y_dead:
            self.last_direction = 'Left' if x < 127 else 'Right'
        elif abs(127 - x) > abs(127 - y):
            self.last_direction = 'Left' if x < 127 else 'Right'
        elif abs(127 - y) > abs(127 - x):
            self.last_direction = 'Up' if y < 127 else 'Down'
        
        return self.last_direction

    # Deleting (Calling destructor)
    def __del__(self):
        self.ADC.close()
        self.BUTTON.close()


if __name__ == "__main__":
    print("Error: Do not run this file. Run snake.py instead.")