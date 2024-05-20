from pathlib import Path
import sys
from gpiozero import LED
import time

HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import * 

USING_GRAVITECH_ADC = False # Only modify this if you are using a Gravitech ADC

BLUE = LED(12)
GREEN = LED(16)
YELLOW = LED(20)
RED = LED(21)
LEDS: list = (BLUE, GREEN, YELLOW, RED)

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
    while True:
        # read the ADC value of channel 0
        value = ADC.analogRead(0)
        print(value / 2.55)
        LEDS_to_light : int = 0

        for i in range (25, 95, 25):
            if value / 2.55 >= i:
                LEDS_to_light += 1

        if value / 255 >= .95:
            LEDS_to_light += 1

        for i in range(LEDS_to_light):
            LEDS[i].on()
        
        for i in range(LEDS_to_light, 4):
            LEDS[i].off()
            
def destroy():
    global ADC,LEDS
    ADC.close()
    for LED in LEDS:
        LED.close()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()