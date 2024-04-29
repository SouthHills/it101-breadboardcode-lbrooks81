from gpiozero import RGBLED, Button
from random import randint
from time import sleep
from signal import pause

LED = RGBLED(red = 13, green = 19, blue = 26)
BUTTON = Button(21)
Running : bool = True

def randomize_colors():
    r=randint(0,100)
    g=randint(0,100)
    b=randint(0,100)
    return (r / 100, g / 100, b / 100)    

def set_color(color : tuple):
    LED.color = (color)

def flash():
    global Running
    Running = False

    # Default color is green
    color : tuple = (1, 0, 1)
    
    
    # Sets color to red if the LED was not green on button press
    if LED.color != (1, 0, 1):
        color = (0, 1, 1)
    
    # Blinky
    for i in range (0, 5):
        set_color((1, 1, 1))
        sleep(.5)
        set_color(color)
        sleep(.5)


def cycle():
    for i in range(0, randint(3,5)):
        if not Running:
            return
        set_color(randomize_colors())
        sleep(randint(0, 4))
    # Last color should be green
    set_color((1, 0, 1))
    
if __name__ == "__main__":
    try:
        BUTTON.when_pressed = flash
        cycle()
        pause()
    except:
        pass
    

    