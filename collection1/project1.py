from gpiozero import Button
import subprocess
import time

FIREFOX_BUTTON = Button(26)
CHROMIUM_BUTTON = Button(21)

firefox_running : bool = False
chromium_running : bool = False
firefox_pid : int
chromium_pid : int

def chromium() -> None:
    global chromium_running, chromium_pid
    if chromium_running == False:
        chromium_pid = subprocess.Popen(["chromium-browser"])    
    else:
        chromium_pid.terminate
    chromium_running = not chromium_running

    
def firefox() -> None:
    global firefox_running, firefox_pid
    if firefox_running == False:
        firefox_pid = subprocess.Popen(["firefox"])
    else:
        firefox_pid.terminate
    firefox_running = not firefox_running


def destroy():
    CHROMIUM_BUTTON.close()
    FIREFOX_BUTTON.close()

if __name__ == "__main__":
    while True:
        try:
            FIREFOX_BUTTON.when_pressed = firefox
            CHROMIUM_BUTTON.when_pressed = chromium
        except KeyboardInterrupt:  # Press ctrl-c to end the program.
            destroy()

