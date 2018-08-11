import pygame
import time
from population import Population
from screen import Screen

# Create the screen
screen = Screen()
frame  = screen.get_frame()
font   = screen.get_font()

# Set up fps
fps = 60
now = time.time()

# Set up game variables
running = True
score   = 0

# Create the population
population = Population()

# Game loop
while running:
    # Refresh screen
    frame.fill((255, 255, 255))

    # Print score
    score_surfice = font.render(str(score), False, (0, 200, 0))
    frame.blit(score_surfice, (Screen.width - 80, 20))

    # Draw walls
    pygame.draw.line(frame, (0, 0, 0), (5, 0), (5, Screen.height), 10)
    pygame.draw.line(frame, (0, 0, 0), (0, 5), (Screen.width, 5), 10)
    pygame.draw.line(frame, (0, 0, 0), (Screen.width - 5, Screen.height), (Screen.width - 5, 0), 10)
    pygame.draw.line(frame, (0, 0, 0), (Screen.width, Screen.height - 5), (0, Screen.height - 5), 10)

    # Draw the population
    population.draw(frame)

    # Move the snakes
    if not population.are_all_dead():
        population.move()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lock to 60fps
    while (time.time() - now) < (1 / fps):
        pass
    now = time.time()
