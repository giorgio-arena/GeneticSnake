from snake import Snake


class Population:
    def __init__(self):
        self.num_snakes = 100
        self.snakes = [Snake() for _ in range(self.num_snakes)]
        self.dead_snakes = 0
        self.all_dead = False

    def are_all_dead(self):
        return self.all_dead

    def move(self, screen_dims, food_pos):
        for snake in self.snakes:
            if not snake.is_dead():
                snake.move(screen_dims, food_pos)
                if snake.is_dead():
                    self.dead_snakes += 1
                    if self.dead_snakes == len(self.snakes):
                        self.all_dead = True

    def draw(self, frame):
        for snake in self.snakes:
            snake.draw(frame)