import numpy as np
from brain import Brain
from screen import Screen
from snake import Snake


class SmartSnake(Snake):
    body_radius  = int(Snake.body_sz / 2)  # remove
    max_starving = 800  # Movements before dying of starvation

    def __init__(self, parent_1=None, parent_2=None):
        super().__init__()
        if parent_1 is None and parent_2 is None:  # Inital random brain
            self._brain = Brain()
        elif parent_2 is None:                     # Top 5 best brains: pass unchanged
            self._brain = Brain(parent_1.brain)
        else:                                      # Crossover
            self._brain = Brain(parent_1.brain, parent_2.brain)

        self._starving_lv = 0
        self._lifetime = 0
        self._fitness = 0

    @property
    def fitness(self):
        return self._fitness

    @property
    def brain(self):
        return self._brain

    def move(self, food_pos):
        """
        :param food_pos:    X and Y coordinates of where the food is

        :return: True if the food has been eaten, False otherwise
        """
        ret = False

        if super().move(food_pos):
            self._starving_lv = 0
            ret = True

        if not self._is_dead:
            self.set_direction(self._brain.think(self.get_visual_inputs(food_pos)))

            self._lifetime += 1
            self._starving_lv += 1

            if self._starving_lv > SmartSnake.max_starving:
                self.die()

        return ret

    def mutate(self):
        self._brain.mutate()

    def die(self):
        super().die()

        # Calculate fitness
        self._fitness = int(np.power(self._lifetime, 2) * np.power(2, np.minimum(self._length, 10)))
        if self._length > 10:
            self._fitness += (self._length - 10) * 1000;

    def get_visual_inputs(self, food_pos):
        """
        :return A list of 24 integers. Every three elements represent what the snake can see from different dirs:
                - The first of the triple contains the distance between its head and the wall
                - The second of the triple contains the distance between its head and the food (if in that dir)
                - The third of the triple contains the distance between its head and its body (if in that dir)

                The snake can see from 8 different angles (relative to the head's current dir) and these will be
                arranged in the following order: [0, 45, 90, 135, 180, 225, 270, 315]
        """
        ret              = []
        (food_x, food_y) = food_pos
        max_distance     = np.maximum(Screen.width, Screen.height)
        multiplier       = -1 / max_distance  # Multiplying this factor by a result and adding one gives range (0, 1)

        dir = self._dirs[0]  # Head's dir
        for i in range(8):
            x_fact = np.sign(np.round(np.cos(np.radians(dir))))
            y_fact = np.sign(np.round(np.sin(np.radians(dir))))

            x_incr = SmartSnake.body_sz * x_fact
            y_incr = SmartSnake.body_sz * y_fact

            (x, y) = (self._x[0], self._y[0])

            # No need to find if food is not in the quarter we're interested in
            food_found = (x_fact > 0 and food_x < x - SmartSnake.body_radius) or (x_fact < 0 and food_x > x + SmartSnake.body_radius) or \
                         (y_fact > 0 and food_y < y - SmartSnake.body_radius) or (y_fact < 0 and food_y > y + SmartSnake.body_radius)
            body_found = self._length == 1  # No need to search if there is no more body

            food_dist = max_distance
            body_dist = max_distance

            while 0 < x < Screen.width and 0 < y < Screen.height and (not food_found or not body_found):
                # If this angle points at food, calculate distance and don't look for food anymore
                if not food_found:
                    if food_x - SmartSnake.body_radius < x < food_x + SmartSnake.body_radius and \
                       food_y - SmartSnake.body_radius < y < food_y + SmartSnake.body_radius:
                        food_dist = int(np.sqrt(pow(self._x[0] - x, 2) + pow(self._y[0] - y, 2)))
                        food_found = True

                # If this angle points at a body part, calculate distance and don't look for body parts anymore
                if not body_found:
                    for j in range(1, self._length):
                        if self._x[j] - SmartSnake.body_radius < x < self._x[j] + SmartSnake.body_radius and \
                           self._y[j] - SmartSnake.body_radius < y < self._y[j] + SmartSnake.body_radius:
                            body_dist = int(np.sqrt(pow(self._x[0] - x, 2) + pow(self._y[0] - y, 2)))
                            body_found = True

                x += x_incr
                y += y_incr

            wall_dist = int(np.sqrt(pow(self._x[0] - x, 2) + pow(self._y[0] - y, 2)))

            ret.append(wall_dist * multiplier + 1)
            ret.append(food_dist * multiplier + 1)
            ret.append(body_dist * multiplier + 1)

            dir += 45

        return ret
