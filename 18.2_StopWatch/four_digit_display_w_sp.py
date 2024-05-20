# Description : Control 4_Digit_7_Segment_Display with 74HC595
from gpiozero import OutputDevice
import time
import threading

# Define the patterns for the characters "0"-"9".
# Due to common anode, 0 means LED on and 1 means LED off.
# Note that the MSB is the decimal point.
NUM_PATTERNS = (
    0b1100_0000, # 0
    0b1111_1001, # 1
    0b1010_0100, # 2
    0b1011_0000, # 3
    0b1001_1001, # 4
    0b1001_0010, # 5
    0b1000_0010, # 6
    0b1111_1000, # 7
    0b1000_0000, # 8
    0b1001_0000  # 9
)

class FourDigitDisplayWithSP:
    outputs: tuple
    msb_first: bool
    data_pin: OutputDevice
    latch_pin: OutputDevice
    clock_pin: OutputDevice
    num_to_display: int = 0
    running: bool = True
    display_thread: threading.Thread = None
    
    def __init__(self, digit_pins: tuple, msb_first: bool, data_pin, latch_pin, clock_pin, initial_number = 0):
        self.outputs = tuple(map(lambda pin: OutputDevice(pin), digit_pins))
        self.msb_first = msb_first
        self.data_pin = OutputDevice(data_pin)
        self.latch_pin = OutputDevice(latch_pin)
        self.clock_pin = OutputDevice(clock_pin)
        self.num_to_display = initial_number
        # Spin up a new thread to run the loop method
        self.display_thread = threading.Thread(target=self.loop, daemon=True)
        self.display_thread.start()
        
    def set_display(self, new_num):
        self.num_to_display = new_num
    
    def __shift_out(self, msb: bool, val):
        for i in range(0, 8):
            self.clock_pin.off()  # Turning off the clock to prepare for sending a bit
            if msb != self.msb_first:
                # If we're sending LSB first, we check each bit of the value from right to left
                #   and send it out accordingly
                if (0x01 & (val >> i) == 0x01):
                    self.data_pin.on()   # If the bit is 1, we turn on the data pin
                else:
                    self.data_pin.off()  # If the bit is 0, we turn off the data pin
            else:
                # If we're sending MSB first, we check each bit of the value from left to right
                #   and send it out accordingly
                if (0x80 & (val << i) == 0x80):
                    self.data_pin.on()   # If the bit is 1, we turn on the data pin
                else:
                    self.data_pin.off()  # If the bit is 0, we turn off the data pin
            self.clock_pin.on()  # Turning on the clock to send the bit
                
    def __outData(self, data):      # function used to output data for 74HC595
        self.latch_pin.off()
        self.__shift_out(self.msb_first, data)
        self.latch_pin.on()
        
    def __selectDigit(self, digit): # Open one of the 7-segment display and close the remaining three
        self.outputs[0].off() if ((digit&0x08) == 0x08) else self.outputs[0].on()
        self.outputs[1].off() if ((digit&0x04) == 0x04) else self.outputs[1].on()
        self.outputs[2].off() if ((digit&0x02) == 0x02) else self.outputs[2].on()
        self.outputs[3].off() if ((digit&0x01) == 0x01) else self.outputs[3].on()
        
    def __display(self, dec):   # display function for 7-segment display
        global NUM_PATTERNS
        time.sleep(0.003)
        self.__outData(0xff)   # eliminate residual display
        self.__selectDigit(0x01)   # Select the first, and display the single digit
        self.__outData(NUM_PATTERNS[dec%10])
        
        time.sleep(0.003)   # display duration
        self.__outData(0xff)
        self.__selectDigit(0x02)   # Select the second, and display the tens digit
        self.__outData(NUM_PATTERNS[dec%100//10])
        
        time.sleep(0.003)
        self.__outData(0xff)
        self.__selectDigit(0x04)   # Select the third, and display the hundreds digit
        self.__outData(NUM_PATTERNS[dec%1000//100])
        
        time.sleep(0.003)
        self.__outData(0xff)
        self.__selectDigit(0x08)   # Select the fourth, and display the thousands digit
        self.__outData(NUM_PATTERNS[dec%10000//1000])
            
    def loop(self):
        while self.running:
            self.__display(self.num_to_display)
            
    def cleanup(self):
        self.__del__()
          
    # Deleting (Calling destructor)
    def __del__(self):
        self.running = False  # Set running flag to False to stop the loop
        if self.display_thread:  # Check if the thread is initialized
            self.display_thread.join()  # Wait for the thread to terminate
        self.data_pin.close()
        self.latch_pin.close()
        self.clock_pin.close()     

if __name__ == '__main__': # Program entrance
    print ('Run stop_watch.py instead.')
 