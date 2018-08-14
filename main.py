import pygame
import time
from population import Population
from screen import Screen

# Create the screen
screen = Screen()

# Create the population
population = Population()

# Set up game variables
fps     = 60
now     = time.time()
running = True

# Game loop
while running:
    # Refresh screen
    screen.frame.fill((255, 255, 255))

    # Draw walls
    pygame.draw.line(screen.frame, (0, 0, 0), (5, 0), (5, Screen.height), 10)
    pygame.draw.line(screen.frame, (0, 0, 0), (0, 5), (Screen.width, 5), 10)
    pygame.draw.line(screen.frame, (0, 0, 0), (Screen.width - 5, Screen.height), (Screen.width - 5, 0), 10)
    pygame.draw.line(screen.frame, (0, 0, 0), (Screen.width, Screen.height - 5), (0, Screen.height - 5), 10)

    # Draw the population
    population.draw(screen.frame)

    # Print generation and current max score
    generation_surfice = screen.font.render("Generation " + str(population.generation), False, (0, 150, 0))
    max_score_surfice  = screen.font.render("Max score  " + str(population.max_score), False, (0, 150, 0))
    screen.frame.blit(generation_surfice, (Screen.width - 200, 20))
    screen.frame.blit(max_score_surfice, (Screen.width - 200, 50))

    # Move the snakes
    population.move()
    if population.are_all_dead:
        population.reproduce()

    # Update display
    pygame.display.flip()

    # Quit on close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lock to 60fps
    while (time.time() - now) < (1 / fps):
        pass
    now = time.time()
