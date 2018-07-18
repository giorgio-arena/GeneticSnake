import pygame
import random
from snake import Snake

snake = Snake()

(width, height) = (640, 480)
mainframe = pygame.display.set_mode((width, height), pygame.DOUBLEBUF|pygame.HWSURFACE)
pygame.display.set_caption('Genetic Snake')
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)  # Comic sans, yay
clock = pygame.time.Clock()

score = 0

(food_pos_x, food_pos_y) = (random.randint(30, width - 30), random.randint(30, height - 30))   # Generate
(food_pos_x, food_pos_y) = ((int(food_pos_x / 20) + 1) * 20, (int(food_pos_y / 20) + 1) * 20)  # Round to multiple

running = True
while running:
    # Refresh screen
    mainframe.fill((255, 255, 255))

    # Print score
    scoresurfice = myfont.render(str(clock.get_fps()), False, (0, 200, 0))
    mainframe.blit(scoresurfice, (width - 80, 20))

    # Draw walls
    pygame.draw.line(mainframe, (0, 0, 0), (5, 0), (5, height), 10)
    pygame.draw.line(mainframe, (0, 0, 0), (0, 5), (width, 5), 10)
    pygame.draw.line(mainframe, (0, 0, 0), (width - 5, height), (width - 5, 0), 10)
    pygame.draw.line(mainframe, (0, 0, 0), (width, height - 5), (0, height - 5), 10)

    # Draw the snake
    snake.draw(mainframe)

    # Draw food
    pygame.draw.circle(mainframe, (255, 0, 0), (food_pos_x, food_pos_y), 5, 0)

    # Move the snake
    if not snake.is_dead():
        if snake.move(width, height, (food_pos_x, food_pos_y)):
            (food_pos_x, food_pos_y) = (random.randint(30, width - 30), random.randint(30, height - 30))
            (food_pos_x, food_pos_y) = ((int(food_pos_x / 20) + 1) * 20, (int(food_pos_y / 20) + 1) * 20)
            score += 1

    pygame.display.flip()
    #clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.set_direction("left")
            elif event.key == pygame.K_UP:
                snake.set_direction("up")
            elif event.key == pygame.K_RIGHT:
                snake.set_direction("right")
            elif event.key == pygame.K_DOWN:
                snake.set_direction("down")
