from pathlib import Path
from gpiozero import RGBLED
from time import sleep

LED = RGBLED(red=13, green=19, blue=26, active_high=True)

path = Path('/sys/class/thermal/thermal_zone0/temp')
temp = path.read_text()

def set_color(r, g, b):
    """ Invert the colors due to using a common anode """
    LED.color = (1 - r, 1 - g, 1 - b)

print(int(temp) / 1000)

if int(temp) / 1000 < 15:
    set_color(0, 0, 1)
if int(temp) / 1000 > 80:
    set_color(1, 0, 0)

sleep(10)