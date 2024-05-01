# Description : Control RGBLED with Potentiometers
from pathlib import Path
import sys
from gpiozero import RGBLED
import time

HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import * 

USING_GRAVITECH_ADC = False # Only modify this if you are using a Gravitech ADC

RED_LED_PIN = 22      # define 3 pins for RGBLED
GREEN_LED_PIN = 27
BLUE_LED_PIN = 17
RGB_LED = RGBLED(red=RED_LED_PIN, green=GREEN_LED_PIN, blue=BLUE_LED_PIN, pwm=True)
ADC = ADCDevice() # Define an ADCDevice class object

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
    global ADC, RGB_LED
    while True:     
        red_value = ADC.analogRead(0)       # read ADC value of 3 potentiometers
        green_value = ADC.analogRead(1)
        blue_value = ADC.analogRead(2)
        
        # map the read value of potentiometers into normalized values (0-1) and set the RGBLED color
        RGB_LED.value = (red_value / 255.0, green_value / 255.0, blue_value / 255.0)
        
        # print read ADC value
        print(f'Red: {red_value} \tGreen: {green_value} \tBlue: {blue_value}')
        time.sleep(0.01)

def destroy():
    global ADC, RGB_LED
    ADC.close()
    RGB_LED.close()
    
if __name__ == '__main__': # Program entrance
    print ('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
