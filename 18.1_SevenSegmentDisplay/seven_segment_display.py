# Description : Control SevenSegmentDisplay with 74HC595
from gpiozero import OutputDevice
import time

LSBFIRST = 1
MSBFIRST = 2
# define the pins for 74HC595
DATA_PIN = OutputDevice(17)      # DS Pin of 74HC595(Pin14)
LATCH_PIN = OutputDevice(27)     # ST_CP Pin of 74HC595(Pin12)
CLOCK_PIN = OutputDevice(22)     # CH_CP Pin of 74HC595(Pin11)

# Define the patterns for the characters "0"-"F".
# Due to common anode, 0 means LED on and 1 means LED off.
# Note that the MSB is the decimal point.
CHAR_PATTERNS = (
    0b1100_0000, # 0
    0b1111_1001, # 1
    0b1010_0100, # 2
    0b1011_0000, # 3
    0b1001_1001, # 4
    0b1001_0010, # 5
    0b1000_0010, # 6
    0b1111_1000, # 7
    0b1000_0000, # 8
    0b1001_0000, # 9
    0b1000_1000, # A
    0b1000_0011, # b
    0b1100_0110, # C
    0b1010_0001, # d
    0b1000_0110, # E
    0b1000_1110  # F
)

def shift_out(order,val):
    """
    Sends data to the 74HC595 chip using serial communication.
    Serial communication is a method of transmitting data one bit at a time, sequentially.

    Args:
        order (int): The order of bits to be sent. Use LSBFIRST or MSBFIRST.
        val (int): The data to be sent as a sequence of bits.
    """
    global LSBFIRST, MSBFIRST, CLOCK_PIN, DATA_PIN
    for i in range(0, 8):
        CLOCK_PIN.off()  # Turning off the clock to prepare for sending a bit
        if order == LSBFIRST:
            # If we're sending LSB first, we check each bit of the value from right to left
            #   and send it out accordingly
            if (0x01 & (val >> i) == 0x01):
                DATA_PIN.on()   # If the bit is 1, we turn on the data pin
            else:
                DATA_PIN.off()  # If the bit is 0, we turn off the data pin
        elif order == MSBFIRST:
            # If we're sending MSB first, we check each bit of the value from left to right
            #   and send it out accordingly
            if (0x80 & (val << i) == 0x80):
                DATA_PIN.on()   # If the bit is 1, we turn on the data pin
            else:
                DATA_PIN.off()  # If the bit is 0, we turn off the data pin
        CLOCK_PIN.on()  # Turning on the clock to send the bit

def loop():
    global LSBFIRST, MSBFIRST, LATCH_PIN
    while True:
        for i in range(0,len(CHAR_PATTERNS)):
            print(hex(i))
            LATCH_PIN.off()
            shift_out(MSBFIRST,CHAR_PATTERNS[i])  # Send serial data to 74HC595
            LATCH_PIN.on()
            time.sleep(0.5)
        for i in range(0,len(CHAR_PATTERNS)):
            print(hex(i) + " .")
            LATCH_PIN.off()
            shift_out(MSBFIRST,CHAR_PATTERNS[i] & 0b0111_1111) # Bitwise AND to display the decimal point
            LATCH_PIN.on()
            time.sleep(0.5)

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