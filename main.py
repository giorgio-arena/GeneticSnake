import pygame as pg
import time
import copy
from gui.button import Button
from food import Food
from population import Population
from screen import Screen
from smart_snake import SmartSnake
from snake import Snake

# Create the screen
screen = Screen()

# GUI stuff
buttons_color    = (180, 200, 220)
text_color       = (0, 0, 0)
btn_play_rect    = pg.Rect(Screen.width / 4, Screen.height / 4, Screen.width / 2, Screen.height / 5)
btn_genetic_rect = pg.Rect(Screen.width / 4, Screen.height / 8 * 5, Screen.width / 2, Screen.height / 5)
btn_play         = Button(buttons_color, text_color, btn_play_rect, "Play")
btn_genetic      = Button(buttons_color, text_color, btn_genetic_rect, "Genetic")

selected_mode = 0  # 0: unselected, 1: play, 2: genetic

# Create the population
num_populations = 1
num_snakes      = 100
populations     = [Population(num_snakes) for _ in range(num_populations)]
best_population = None
best_snake      = None

# Single player snake
snake = Snake()
food  = Food()  # also for best in population

# Set up game variables
fps          = 60
now          = time.time()
running      = True
showing_best = False

# Game loop
while running:
    # Refresh screen
    screen.frame.fill((255, 255, 255))

    if selected_mode is 1 or (selected_mode is 2 and showing_best):
        # Draw walls
        pg.draw.line(screen.frame, (0, 0, 0), (5, 0), (5, Screen.height), 10)
        pg.draw.line(screen.frame, (0, 0, 0), (0, 5), (Screen.width, 5), 10)
        pg.draw.line(screen.frame, (0, 0, 0), (Screen.width - 5, Screen.height), (Screen.width - 5, 0), 10)
        pg.draw.line(screen.frame, (0, 0, 0), (Screen.width, Screen.height - 5), (0, Screen.height - 5), 10)

    if selected_mode is 0:
        btn_play.draw(screen.frame, screen.font)
        btn_genetic.draw(screen.frame, screen.font)
    elif selected_mode is 1:
        if not snake.is_dead:
            snake.draw(screen.frame)
            food.draw(screen.frame)

            score_surface = screen.font.render("Score: " + str(snake.length), False, (0, 150, 0))
            screen.frame.blit(score_surface, (Screen.width - 140, 20))

            if snake.move(food.pos()):  # food eaten
                food.change_pos()
            if snake.is_dead:
                break

            # Lock to 60fps
            while (time.time() - now) < (1 / fps):
                pass
            now = time.time()
    elif selected_mode is 2:
        if showing_best:
            # Print generation and current max score
            generation_surface = screen.font.render("Generation " + str(best_population.generation), False, (0, 150, 0))
            score_surface      = screen.font.render("Score " + str(best_snake.length), False, (0, 150, 0))
            screen.frame.blit(generation_surface, (Screen.width - 200, 20))
            screen.frame.blit(score_surface, (Screen.width - 200, 50))

            # Print best snake
            best_snake.draw(screen.frame)
            food.draw(screen.frame)

            # Move snake if alive
            if not best_snake.is_dead:
                if best_snake.move(food.pos()):
                    food.change_pos()
            else:
                for population in populations:
                    population.reproduce()
                showing_best = False

            # Lock to 60fps
            while (time.time() - now) < (1 / fps):
                pass
            now = time.time()

        else:

            loading_surface = screen.font.render("Loading...", False, (0, 0, 0))
            screen.frame.blit(loading_surface, (Screen.width / 2 - 50, Screen.height / 2 - 50))

            # Move the snakes
            num_dead_populations = 0
            for population in populations:
                population.move()
                if population.are_all_dead:
                    num_dead_populations += 1

            # If all populations are dead, get the best snake and show it in the next iteration
            if num_dead_populations == num_populations:
                best_population = copy.deepcopy(populations[0])
                for i in range(1, num_populations):
                    if populations[i].best_snake.fitness > best_population.best_snake.fitness:
                        best_population = copy.deepcopy(populations[i])

                print("Best ever : " + str(best_population.best_snake.fitness) + " " + str(best_population.best_snake.length) + " " + str(best_population.best_snake._lifetime))
                print("Local best: " + str(best_population._snakes[0].fitness) + " " + str(best_population._snakes[0].length) + " " + str(best_population._snakes[0]._lifetime))

                best_snake = SmartSnake(best_population.best_snake)
                food.change_pos()

                showing_best = True

    # Update display
    pg.display.flip()

    # Quit on close button
    for event in pg.event.get():
        if selected_mode is 0:
            if event.type == pg.MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                if btn_play.mouse_over(mouse_pos):
                    selected_mode = 1
                elif btn_genetic.mouse_over(mouse_pos):
                    selected_mode = 2
        elif selected_mode is 1:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    snake.set_direction(0)
                elif event.key == pg.K_DOWN:
                    snake.set_direction(1)
                elif event.key == pg.K_LEFT:
                    snake.set_direction(2)
                elif event.key == pg.K_RIGHT:
                    snake.set_direction(3)

        if event.type == pg.QUIT:
            running = False

