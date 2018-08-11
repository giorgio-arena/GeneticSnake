from food import Food
from snake import Snake


class Population:

    num_snakes = 100

    def __init__(self):
        self.snakes      = [Snake() for _ in range(Population.num_snakes)]
        self.food        = [Food() for _ in range(Population.num_snakes)]
        self.dead_snakes = 0
        self.all_dead    = False

    def are_all_dead(self):
        return self.all_dead

    def move(self):
        for snake, food in zip(self.snakes, self.food):
            if not snake.is_dead():
                if snake.move(food.dims()):
                    food.change_pos()
                if snake.is_dead():
                    self.dead_snakes += 1
                    if self.dead_snakes == Population.num_snakes:
                        self.all_dead = True

    def draw(self, frame):
        for snake, food in zip(self.snakes, self.food):
            snake.draw(frame)
            food.draw(frame)
