# NOTE: If running the game gives you an error, run either "sudo apt install python3-pygame" OR "pip install pygame" in the terminal.

import pygame
import time
import random

pygame.init()

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
    elif event.key == pygame.K_ESCAPE: # Escape pauses the game
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
                    new_direction = do_keypress_event(event, direction) 
                    direction = new_direction if new_direction != None else direction

            # Move the snake
            x, y = snake_list[0]
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
