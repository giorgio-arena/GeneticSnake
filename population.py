import random
from food import Food
from snake import Snake


class Population:
    num_snakes = 100

    def __init__(self):
        self._snakes       = [Snake() for _ in range(Population.num_snakes)]
        self._food         = [Food() for _ in range(Population.num_snakes)]
        self._generation   = 1
        self._max_score    = 1
        self._dead_snakes  = 0
        self._are_all_dead = False

    @property
    def generation(self):
        return self._generation

    @property
    def max_score(self):
        return self._max_score

    @property
    def are_all_dead(self):
        return self._are_all_dead

    def move(self):
        for snake, food in zip(self._snakes, self._food):
            if not snake.is_dead:
                if snake.move(food.dims()):  # food eaten
                    food.change_pos()
                    if snake.length > self._max_score:
                        self._max_score = snake.length
                if snake.is_dead:
                    self._dead_snakes += 1
                    if self._dead_snakes == Population.num_snakes:
                        self._are_all_dead = True

    def reproduce(self):
        assert self._are_all_dead is True

        # Sort snakes by fitness
        self._snakes.sort(key=lambda x: x.fitness, reverse=True)

        # The best snake is passed unchanged
        # The best 5% (except first) are not crossed over but are mutated
        five_percent  = int(Population.num_snakes / 20)
        total_fitness = sum(snake.fitness for snake in self._snakes)

        # Crossover
        new_snakes = []
        for i in range(Population.num_snakes):
            if i < five_percent:
                new_snakes.append(Snake(self._snakes[i]))  # pass unchanged
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
                new_snakes.append(Snake(self._snakes[chosen_1], self._snakes[chosen_2]))

            if i is not 0:
                new_snakes[-1].mutate()

        # Replace old snakes with descendents
        for i in range(Population.num_snakes):
            self._snakes[i] = new_snakes[i]
            self._food[i]   = Food()

        # Reset attributes
        self._dead_snakes  = 0
        self._are_all_dead = False
        self._max_score    = 1
        self._generation  += 1

    def draw(self, frame):
        if self._generation == 1:
            for snake, food in zip(self._snakes, self._food):
                snake.draw(frame)
                food.draw(frame)
        else:
            self._snakes[0].draw(frame)
            self._food[0].draw(frame)
