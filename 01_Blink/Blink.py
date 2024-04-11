from gpiozero import LED as LEDClass # Alias
import time

LED_17 = LEDClass(17)  # define led
LED_18 = LEDClass(18)

def loop():
    global LED_17
    while True:
        LED_17.on()
        LED_18.off() 
        print ("led turned on >>>") # print information on terminal
        time.sleep(1)
        LED_17.off()
        LED_18.on()
        print ("led turned off <<<")
        time.sleep(1)
        
def destroy():
    global LED_17
    # Release resources
    LED_17.close()
    LED_18.close()

if __name__ == "__main__":    # Program start point
    print("Program is starting ... \n")
    print(f"Using pin {LED_17.pin}")
    try:
        loop()
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()
