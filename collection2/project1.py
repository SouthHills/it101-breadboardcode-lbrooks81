import subprocess
from gpiozero import LED
from time import sleep

RED = LED(18)
GREEN = LED(19)

def is_internet_connected() -> bool:
    try:
    # Run the ping command with a timeout of 2 seconds and count 1 packet
        subprocess.check_output(['ping', '-c', '1', '-W', '2', 'www.google.com'])
        return True
    except subprocess.CalledProcessError:
        return False

def destroy():
    RED.close()
    GREEN.close()
    
if __name__ == '__main__':     # Program entrance
    print ('Program is starting ... ')
    while True:
        try:
            if is_internet_connected():
                RED.off()
                GREEN.on()
            else:
                GREEN.off()
                RED.on()
            sleep(5)

        except KeyboardInterrupt:  # Press ctrl-c to end the program.
            destroy()
            break

