# Description : Control 4_Digit_7_Segment_Display with 74HC595
from gpiozero import OutputDevice
import time
from four_digit_display_w_sp import FourDigitDisplayWithSP

MSBFIRST = True
# define the pins for 74HC595
DATA_PIN = 24      # DS Pin of 74HC595(Pin14)
LATCH_PIN = 23     # ST_CP Pin of 74HC595(Pin12)
CLOCK_PIN = 18     # CH_CP Pin of 74HC595(Pin11)

DIGIT_PINS = (17, 22, 27,10) # If your digits are out of order, rearrange this tuple

DISPLAY = FourDigitDisplayWithSP(DIGIT_PINS, MSBFIRST, DATA_PIN, LATCH_PIN, CLOCK_PIN, 0)

counter = 0  # This number will be dislayed by 7-segment display
    
def initial_test():
    global DISPLAY
    print("Printing 1234 to the LED display...")
    DISPLAY.set_display(1234)
    time.sleep(2)
    print("Printing 8888 to the LED display...")
    DISPLAY.set_display(8888)
    time.sleep(2)
          
def loop():
    global DISPLAY, counter
    while True:
        DISPLAY.set_display(counter)
        print(counter)
        time.sleep(1)
        counter += 1
        
def destroy():  
    DISPLAY.cleanup()      

if __name__ == '__main__': # Program entrance
    print ('Program is starting...')
    try:
        initial_test()
        loop()  
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()
 