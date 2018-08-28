import copy
import random
from food import Food
from smart_snake import SmartSnake


class Population:
    def __init__(self, num_snakes):
        self._num_snakes   = num_snakes
        self._snakes       = [SmartSnake() for _ in range(num_snakes)]
        self._food         = [Food() for _ in range(num_snakes)]
        self._generation   = 1
        self._max_score    = 1
        self._dead_snakes  = 0
        self._are_all_dead = False
        self._best_snake   = SmartSnake()

    @property
    def generation(self):
        return self._generation

    @property
    def max_score(self):
        return self._max_score

    @property
    def best_snake(self):
        return self._best_snake

    @property
    def are_all_dead(self):
        return self._are_all_dead

    def move(self):
        for snake, food in zip(self._snakes, self._food):
            if not snake.is_dead:
                if snake.move(food.pos()):  # food eaten
                    food.change_pos()
                    if snake.length > self._max_score:
                        self._max_score = snake.length
                if snake.is_dead:
                    self._dead_snakes += 1
                    if self._dead_snakes == self._num_snakes:
                        # Sort snakes by fitness
                        self._snakes.sort(key=lambda x: x.fitness, reverse=True)
                        if self._snakes[0].fitness > self._best_snake.fitness:
                            self._best_snake = copy.deepcopy(self._snakes[0])
                        self._are_all_dead = True

    def reproduce(self):
        assert self._are_all_dead is True

        # The global and local best snakes are passed unchanged
        # The best 10% (except first two) are not crossed over but are mutated
        ten_percent    = int(self._num_snakes / 10)
        twenty_percent = int(self._num_snakes / 5)
        for i in range(twenty_percent):
            self._snakes[-i].fitness = 0
        total_fitness = sum(snake.fitness for snake in self._snakes)

        # Crossover
        new_snakes = [SmartSnake(self._best_snake)]
        for i in range(self._num_snakes - 1):
            if i < ten_percent:
                new_snakes.append(SmartSnake(self._snakes[i]))  # pass unchanged
            elif i > self._num_snakes - twenty_percent:
                new_snakes.append(SmartSnake())
            else:
                # Choose parent 1
                probab_1 = random.randint(0, total_fitness)
                chosen_1 = 0
                while probab_1 - self._snakes[chosen_1].fitness > 0:
                    probab_1 -= self._snakes[chosen_1].fitness
                    chosen_1 += 1

                # Choose parent 2
                probab_2 = random.randint(0, total_fitness)
                chosen_2 = 0
                while probab_2 - self._snakes[chosen_2].fitness > 0:
                    probab_2 -= self._snakes[chosen_2].fitness
                    chosen_2 += 1

                # Crossover
                new_snakes.append(SmartSnake(self._snakes[chosen_1], self._snakes[chosen_2]))

            if i is not 0:
                new_snakes[-1].mutate()

        # Replace old snakes with descendents
        for i in range(self._num_snakes):
            self._snakes[i] = SmartSnake(new_snakes[i])
            self._food[i]   = Food()

            snake_x, snake_y = self._snakes[i].head_pos()
            food_x, food_y   = self._food[i].pos()
            while food_x - SmartSnake.body_radius <= snake_x <= food_x + SmartSnake.body_radius and \
                  food_y - SmartSnake.body_radius <= snake_y <= food_y + SmartSnake.body_radius:
                self._food[i] = Food()
                food_x, food_y = self._food[i].pos()

        # Reset attributes
        self._dead_snakes  = 0
        self._are_all_dead = False
        self._max_score    = 1
        self._generation  += 1
