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
    
def shift_out(order,val):
    """
    Sends data to the 74HC595 chip using serial communication.
    Serial communication is a method of transmitting data one bit at a time, sequentially.

    Args:
        order (int): The order of bits to be sent. Use LSBFIRST or MSBFIRST.
        val (int): The data to be sent as a sequence of bits.
    """
    global LSBFIRST, MSBFIRST, CLOCK_PIN, DATA_PIN
    debug_print_out: str = "["
    for i in range(0, 8):
        CLOCK_PIN.off()  # Turning off the clock to prepare for sending a bit
        if order == LSBFIRST:
            # If we're sending LSB first, we check each bit of the value from right to left
            #   and send it out accordingly
            if (0x01 & (val >> i) == 0x01):
                DATA_PIN.on()   # If the bit is 1, we turn on the data pin
                debug_print_out += "X, "
            else:
                DATA_PIN.off()  # If the bit is 0, we turn off the data pin
                debug_print_out += "O, "
        elif order == MSBFIRST:
            # If we're sending MSB first, we check each bit of the value from left to right
            #   and send it out accordingly
            if (0x80 & (val << i) == 0x80):
                DATA_PIN.on()   # If the bit is 1, we turn on the data pin
                debug_print_out += "X, "
            else:
                DATA_PIN.off()  # If the bit is 0, we turn off the data pin
                debug_print_out += "O, "
        CLOCK_PIN.on()  # Turning on the clock to send the bit
    debug_print_out = debug_print_out[:-2] + "]"
    print(debug_print_out)

def loop():
    """
    This function controls the sequence of LED lighting using the 74HC595 chip.
    """
    global LSBFIRST, MSBFIRST, LATCH_PIN
    while True:
        x = 0x01  # Starting with the first LED lit
        for _ in range(0, 8):
            LATCH_PIN.off()         # Turning off the latch to prepare for updating data
            shift_out(LSBFIRST, x)  # Sending the current LED pattern to the chip
            LATCH_PIN.on()          # Turning on the latch to update the LED outputs
            x <<= 1                 # Shifting the pattern to the left to light up the next LED
            time.sleep(0.1)         # Waiting for a short time before the next LED
        x = 0x80  # Starting with the last LED lit
        for _ in range(0, 8):
            LATCH_PIN.off()         # Turning off the latch to prepare for updating data
            shift_out(LSBFIRST, x)  # Sending the current LED pattern to the chip
            LATCH_PIN.on()          # Turning on the latch to update the LED outputs
            x >>= 1                 # Shifting the pattern to the right to light up the previous LED
            time.sleep(0.1)         # Waiting for a short time before the next LED

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
