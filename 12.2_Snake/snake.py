# NOTE: If running the game gives you an error, run either "sudo apt install python3-pygame" OR "pip install pygame" in the terminal.

import pygame
import time
import random
from gpiozero import Button
from pathlib import Path
import sys

HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import * 

pygame.init()

# Define device pins
BUTTON = Button(18)
ADC = ADCDevice()

# Set up the display
GRID_SIZE = 28
GRID_WIDTH, GRID_HEIGHT = 28, 24  # 28 columns x 24 rows
WIDTH, HEIGHT = GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Score: 0")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Snake and food sizes
SNAKE_SPEED = 10

# Fonts
FONT = pygame.font.SysFont(None, 25)

# Pause variable
PAUSED = False

# Detect ADC address
def __init__(self):
        if(self.ADC.detectI2C(0x48) and self.USING_GRAVITECH_ADC): 
            self.ADC = GravitechADC()
        elif(self.ADC.detectI2C(0x48)): # Detect the pcf8591.
            self.ADC = PCF8591()
        elif(self.ADC.detectI2C(0x4b)): # Detect the ads7830
            self.ADC = ADS7830()
        else:
            print("No correct I2C address found, \n"
                "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
                "Program Exit. \n")
            exit(-1)

def get_direction(self, x = None, y = None):
    # If this method has been called seperately from get_xy_pos(), x and y need values
    if x == None or y == None:
        x = self.ADC.analogRead(1)           # read analog value of axis X and Y
        y = self.ADC.analogRead(0)
    
    DEAD_ZONE_RANGE = (100, 152)
    x_dead: bool = False
    y_dead: bool = False
    
    if (x == 0 and y == 0) or (x == 255 or y == 255):
        return self.last_direction
    
    if DEAD_ZONE_RANGE[0] <= x <= DEAD_ZONE_RANGE[1]:
        x_dead = True
        
    if DEAD_ZONE_RANGE[0] <= y <= DEAD_ZONE_RANGE[1]:
        y_dead = True
        
    if x_dead and y_dead:
        self.last_direction = 'Neutral'
    elif x_dead:
        self.last_direction = 'Up' if y < 127 else 'Down'
    elif y_dead:
        self.last_direction = 'Left' if x < 127 else 'Right'
    elif abs(127 - x) > abs(127 - y):
        self.last_direction = 'Left' if x < 127 else 'Right'
    elif abs(127 - y) > abs(127 - x):
        self.last_direction = 'Up' if y < 127 else 'Down'
    return self.last_direction

def get_button_pressed(self):
    button_pressed = self.BUTTON.is_active
    if button_pressed and not self.button_pressed_momentary:
        self.button_pressed_momentary = True
    else:
        self.button_pressed_momentary = False
    return self.button_pressed_momentary

# Function to draw snake
def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(WINDOW, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Function to display message
def message(msg, color):
    mesg = FONT.render(msg, True, color)
    WINDOW.blit(mesg, [WIDTH / 6, HEIGHT / 3])

# Function to generate random food position
def generate_food():
    return random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT)

def do_keypress_event(event, current_direction):
    global PAUSED
    # Can't double-back on your snake
    if event.key == pygame.K_LEFT and current_direction != "RIGHT":
        return "LEFT"
    elif event.key == pygame.K_RIGHT and current_direction != "LEFT":
        return "RIGHT"
    elif event.key == pygame.K_UP and current_direction != "DOWN":
        return "UP"
    elif event.key == pygame.K_DOWN and current_direction != "UP":
        return "DOWN"
    elif event.key == Button.when_activated: # Pressing the button pauses the game
        PAUSED = True

# Function to main loop
def game_loop():
    global PAUSED
    game_over = False
    game_close = False

    while True:
        
        # Reset the title tab
        pygame.display.set_caption("Snake Game - Score: 0")
        
        # Initial snake position (// performs division and rounds down)
        snake_list = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        length_of_snake = 1

        # Initial direction
        direction = "RIGHT"

        # Food position
        food_x, food_y = generate_food()

        # Score
        score = 0

        # Main game loop
        while not game_over:

            # Pause mechanism
            while PAUSED:
                WINDOW.fill(BLACK)
                message("Paused. Press [Space] to continue or [Escape] to quit.", WHITE)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            PAUSED = False
                        elif event.key == pygame.K_ESCAPE:
                            # Straight kill the game
                            pygame.quit() # Kill game
                            quit() # Kill program

            # Input handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # An attempt to close the window or program
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    new_direction = get_direction() 
                    direction = new_direction if new_direction != None else direction

            # Move the snake
            x = ADC.analogRead(1)      # read analog value of axis X and Y
            y = ADC.analogRead(0)
            if direction == "RIGHT":
                x += 1
            elif direction == "LEFT":
                x -= 1
            elif direction == "UP":
                y -= 1
            elif direction == "DOWN":
                y += 1

            # Check for collision with walls or self
            if x >= GRID_WIDTH or x < 0 or y >= GRID_HEIGHT or y < 0 or (x, y) in snake_list[1:]:
                game_over = True
                game_close = True

            # Check if snake eats food
            if x == food_x and y == food_y:
                food_x, food_y = generate_food()
                length_of_snake += 1
                score += 1
                pygame.display.set_caption(f"Snake Game - Score: {score}")
            else:
                snake_list.pop()

            # Update snake position
            snake_list.insert(0, (x, y))

            # Drawing
            WINDOW.fill(BLACK)
            pygame.draw.rect(WINDOW, RED, (food_x * GRID_SIZE, food_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            draw_snake(snake_list)

            pygame.display.update()

            # Game speed
            pygame.time.Clock().tick(SNAKE_SPEED)

        # End game message
        while game_close:
            WINDOW.fill(BLACK)
            message("Game Over! Press [Space] to play again or [Escape] to quit.", WHITE)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # Kill game
                    quit() # Kill program
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_close = False
                        game_over = True
                    if event.key == pygame.K_SPACE:
                        game_close = False
                        game_over = False

        if game_over:
            pygame.quit() # Kill game
            quit() # Kill program

if __name__ == '__main__':
    print ('Program is starting ... ') # Program entrance
    try:
        game_loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        pass
