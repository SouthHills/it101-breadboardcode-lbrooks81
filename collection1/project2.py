from gpiozero import LED
from time import sleep

RED = LED(26)
YELLOW = LED(19)
GREEN = LED(13)

def led(LED : LED, seconds : int):
    LED.on()
    sleep(seconds)
    LED.off()

def destroy():
    RED.close()
    YELLOW.close()
    GREEN.close()

if __name__ == "__main__":
    while True:
        try:
            led(RED, 5)
            led(YELLOW, 7)
            led(GREEN, 2)
        except KeyboardInterrupt:
            destroy()

    
    