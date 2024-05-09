# Control LEDMatrix with 74HC595
from gpiozero import OutputDevice
import time

LSBFIRST = 1
MSBFIRST = 2
# define the pins connect to 74HC595
DATA_PIN   = OutputDevice(17)      # DS Pin of 74HC595(Pin14)
LATCH_PIN  = OutputDevice(27)      # ST_CP Pin of 74HC595(Pin12)
CLOCK_PIN  = OutputDevice(22)      # CH_CP Pin of 74HC595(Pin11)
FACE = [0x1c,0x22,0x51,0x45,0x45,0x51,0x22,0x1c]  # data for smiling face
DATA = [     # data of "0-F"
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # " "
    0x00, 0x00, 0x3E, 0x41, 0x41, 0x3E, 0x00, 0x00, # "0"
    0x00, 0x00, 0x21, 0x7F, 0x01, 0x00, 0x00, 0x00, # "1"
    0x00, 0x00, 0x23, 0x45, 0x49, 0x31, 0x00, 0x00, # "2"
    0x00, 0x00, 0x22, 0x49, 0x49, 0x36, 0x00, 0x00, # "3"
    0x00, 0x00, 0x0E, 0x32, 0x7F, 0x02, 0x00, 0x00, # "4"
    0x00, 0x00, 0x79, 0x49, 0x49, 0x46, 0x00, 0x00, # "5"
    0x00, 0x00, 0x3E, 0x49, 0x49, 0x26, 0x00, 0x00, # "6"
    0x00, 0x00, 0x60, 0x47, 0x48, 0x70, 0x00, 0x00, # "7"
    0x00, 0x00, 0x36, 0x49, 0x49, 0x36, 0x00, 0x00, # "8"
    0x00, 0x00, 0x32, 0x49, 0x49, 0x3E, 0x00, 0x00, # "9"   
    0x00, 0x00, 0x3F, 0x44, 0x44, 0x3F, 0x00, 0x00, # "A"
    0x00, 0x00, 0x7F, 0x49, 0x49, 0x36, 0x00, 0x00, # "B"
    0x00, 0x00, 0x3E, 0x41, 0x41, 0x22, 0x00, 0x00, # "C"
    0x00, 0x00, 0x7F, 0x41, 0x41, 0x3E, 0x00, 0x00, # "D"
    0x00, 0x00, 0x7F, 0x49, 0x49, 0x41, 0x00, 0x00, # "E"
    0x00, 0x00, 0x7F, 0x48, 0x48, 0x40, 0x00, 0x00, # "F"
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # " "
]
    
def shiftOut(order,val):
    global LSBFIRST, MSBFIRST, CLOCK_PIN
    for i in range(0,8):
        CLOCK_PIN.off()
        if(order == LSBFIRST):
            DATA_PIN.on() if (0x01&(val>>i)==0x01) else DATA_PIN.off()
        elif(order == MSBFIRST):
            DATA_PIN.on() if (0x80&(val<<i)==0x80) else DATA_PIN.off()
        CLOCK_PIN.on()

def loop():
    global LATCH_PIN, MSBFIRST, DATA, FACE
    while True:
        for _ in range(0,500): # Repeat enough times to display the "smiling face" a period of time
            x=0x80
            for i in range(0,8):
                LATCH_PIN.off()
                shiftOut(MSBFIRST,FACE[i]) #first shift data of line information to first stage 74HC959

                shiftOut(MSBFIRST,~x) #then shift data of column information to second stage 74HC959
                LATCH_PIN.on()         # Output data of two stage 74HC595 at the same time
                time.sleep(0.001) # display the next column
                x>>=1
        for k in range(0,len(DATA)-8): #len(data) total number of "0-F" columns 
            for _ in range(0,20): # times of repeated displaying LEDMatrix in every frame, the bigger the "j", the longer the display time.
                x=0x80      # Set the column information to start from the first column
                for i in range(k,k+8):
                    LATCH_PIN.off()
                    shiftOut(MSBFIRST,DATA[i])
                    shiftOut(MSBFIRST,~x)
                    LATCH_PIN.on()
                    time.sleep(0.001)
                    x>>=1

def destroy():
    global DATA_PIN, LATCH_PIN, CLOCK_PIN
    DATA_PIN.close()
    LATCH_PIN.close()
    CLOCK_PIN.close()

if __name__ == '__main__':  # Program entrance
    print ('Program is starting...')
    try:
        loop()  
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()
        print("Ending program")
