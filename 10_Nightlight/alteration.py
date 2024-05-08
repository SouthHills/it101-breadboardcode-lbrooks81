from gpiozero import LEDBarGraph
from pathlib import Path
import sys
from gpiozero import PWMLED
import time

HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import * 

USING_GRAVITECH_ADC = False # Only modify this if you are using a Gravitech ADC

LED_PINS : list[int] = [25, 12, 16, 24, 23, 20, 21, 0, 1, 18]
LEDS = LEDBarGraph(*LED_PINS, active_high=False)
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
    global ADC, LEDS
    while True:
        value = ADC.analogRead(0)   # read the ADC value of channel 0
        LEDs_to_light : int = 0

        for i in range(10):
            if value > 255/10 * i:
                LEDs_to_light = i

        
        for x in range(LEDs_to_light):
            LEDS[x].on()

        for x in range(LEDs_to_light + 1, 10):
            LEDS[x].off()

        voltage = value / 255.0 * 3.3
        print(f'ADC Value: {value} \tVoltage: {voltage:.2f} \t LEDs to Light: {LEDs_to_light}')
        time.sleep(0.01)

def destroy():
    global ADC, LEDS
    ADC.close()
    LEDS.close()
        
if __name__ == '__main__':   # Program entrance
    print ('Program is starting... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
        



