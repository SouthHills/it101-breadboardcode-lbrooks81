# Description : Control LED with 74HC595
from gpiozero import OutputDevice # A generic GPIO output device that extends GPIODevice
import time

# Defines the data bit that is transmitted preferentially in the shift_out function.
LSBFIRST = 1
MSBFIRST = 2

# define the pins for 74HC595
DATA_PIN = OutputDevice(17)      # DS Pin of 74HC595(Pin14)
LATCH_PIN = OutputDevice(27)     # ST_CP Pin of 74HC595(Pin12)
CLOCK_PIN = OutputDevice(22)     # CH_CP Pin of 74HC595(Pin11)
    
def update_leds(led_index):
    """
    Update the LEDs connected to the 74HC595 chip.

    Args:
        led_index (int): The index of the LED to turn on.
    """
    global DATA_PIN, LATCH_PIN
    debug_print_out: str = "["
    for i in range(8):
        DATA_PIN.value = (i == led_index)   # Turn on the LED at led_index, turn off others
        debug_print_out += ("X" if i == led_index else "O") + ", "
        CLOCK_PIN.on()      # Clock pulse to shift the data
        CLOCK_PIN.off()     # Turn off the clock
    LATCH_PIN.on()      # Update the LED outputs
    LATCH_PIN.off()     # Turn off the latch
    debug_print_out = debug_print_out[:-2] + "]"
    print(debug_print_out)

def loop():
    while True:
        # Moving LED from left to right
        for i in range(8):
            update_leds(i)  # Turn on one LED at a time
            time.sleep(0.1) # Wait for a short duration
        # Moving LED from right to left
        for i in range(7, -1, -1):
            update_leds(i)  # Turn on one LED at a time
            time.sleep(0.1) # Wait for a short duration

def destroy():   
    global DATA_PIN, LATCH_PIN, CLOCK_PIN
    DATA_PIN.close()
    LATCH_PIN.close()
    CLOCK_PIN.close()

if __name__ == '__main__': # Program entrance
    print ('Program is starting...' )
    try:
        loop()  
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()  
