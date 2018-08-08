import pygame
import random
import time
from population import Population

population = Population()

(width, height) = (640, 480)
mainframe = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption('snAIk')
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)  # Comic sans, yay
clock = pygame.time.Clock()

score = 0

(food_pos_x, food_pos_y) = (random.randint(30, width - 30), random.randint(30, height - 30))   # Generate
(food_pos_x, food_pos_y) = ((int(food_pos_x / 20) + 1) * 20, (int(food_pos_y / 20) + 1) * 20)  # Round to multiple

fps = 60
now = time.time()

running = True
while running:
    # Refresh screen
    mainframe.fill((255, 255, 255))

    # Print score
    scoresurfice = myfont.render(str(score), False, (0, 200, 0))
    mainframe.blit(scoresurfice, (width - 80, 20))

    # Draw walls
    pygame.draw.line(mainframe, (0, 0, 0), (5, 0), (5, height), 10)
    pygame.draw.line(mainframe, (0, 0, 0), (0, 5), (width, 5), 10)
    pygame.draw.line(mainframe, (0, 0, 0), (width - 5, height), (width - 5, 0), 10)
    pygame.draw.line(mainframe, (0, 0, 0), (width, height - 5), (0, height - 5), 10)

    # Draw the snakes
    population.draw(mainframe)

    # Draw food
    pygame.draw.circle(mainframe, (255, 0, 0), (food_pos_x, food_pos_y), 5, 0)

    # Move the snakes
    if not population.are_all_dead():
        population.move((width, height), (food_pos_x, food_pos_y))
        '''
        (food_pos_x, food_pos_y) = (random.randint(30, width - 30), random.randint(30, height - 30))
        (food_pos_x, food_pos_y) = ((int(food_pos_x / 20) + 1) * 20, (int(food_pos_y / 20) + 1) * 20)
        score += 1
        '''

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lock to 60fps
    while (time.time() - now) < (1 / fps):
        pass

    now = time.time()
