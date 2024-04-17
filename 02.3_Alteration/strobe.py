from gpiozero import LED as LEDClass, Button
from signal import pause
from time import sleep

LED = LEDClass(17)  # define ledPin
BUTTON = Button(18)  # define buttonPin
Pressed : bool = False

def loop():
    while True:
        if Pressed:
            sleep(.5)
            LED.toggle()
            sleep(.5)
            LED.toggle()
        else: 
            break

def changeLedState():
    global Pressed
    Pressed = not Pressed
    
def destroy():
    global LED, BUTTON
    # Release resources
    LED.close()
    BUTTON.close()

if __name__ == "__main__":     # Program entrance
    print ("Program is starting...")
    while True:
        try:
            # If the button gets pressed, call the function
            # This is an event
            BUTTON.when_pressed = changeLedState
            loop()
        except KeyboardInterrupt:  # Press ctrl-c to end the program.
            destroy()
    