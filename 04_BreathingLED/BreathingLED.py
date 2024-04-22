from gpiozero import PWMLED
import time

LED = PWMLED(18)  # define PWMLED

def loop():
    global LED
    while True:
        i : int = 0
        # range() only works with integers
        for i in range(0, 10): # make the led brighter
            # led.value only accepts floats
            LED.value = i / 10 # set DC (direct current) value as the duty cycle
            time.sleep(0.1)
            
        for i in range(10, 0, -1): # dim the led
            LED.value = i / 10 # set DC value as the duty cycle
            time.sleep(0.1)

def destroy():
    global LED
    LED.close()

if __name__ == '__main__':     # Program entrance
    print ('Program is starting ... ')
    print(f"Using pin {LED.pin}")
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
