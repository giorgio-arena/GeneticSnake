import numpy as np
import pygame
from brain import Brain
from screen import Screen


class Snake:
    body_radius  = 10               # Radius of each circle (body part)
    body_size    = 2 * body_radius  # Diameter of each circle (body part)
    speedup_rate = 0.03             # Percentage of velocity gain
    max_starving = 400              # Movements before dying of starvation

    def __init__(self, parent_1=None, parent_2=None):
        if parent_1 is None and parent_2 is None:  # Inital random brain
            self._brain = Brain()
        elif parent_2 is None:                     # Top 5 best brains: pass unchanged
            self._brain = Brain(parent_1.brain)
        else:                                      # Crossover
            self._brain = Brain(parent_1.brain, parent_2.brain)

        # Positional attributes
        self._x      = [int(Screen.width / 2)]   # List of x coordinates for each of the snake's body parts
        self._y      = [int(Screen.height / 2)]  # List of y coordinates for each of the snake's body parts
        self._length = 1

        self._visual_x = [int(Screen.width / 2)]
        self._visual_y = [int(Screen.height / 2)]

        # Movement attributes
        self._directions     = [0]   # Directions for each of the snake's body parts: 0 right, 90 down, 180 left, 270 up
        self._next_direction = 0     # What the head's next direction will be
        self._velocity       = 3.0  # How many pixels the snake will travel per frame (1 is maximum)
        self._accum          = 0.0   # Don't move the snake until < 1, then move by and subtract 1

        # Snake's look
        self._color       = (0, 0, 0)             # RGB color for the snake's body
        self._head_color  = (0, 100, 0)           # RGB color for the snake's head

        # Frames before moving to a next direction
        self._timer = Snake.body_size

        self._starving_lv = 0

        self._lifetime = 0
        self._fitness = 0

        # Flags
        self._is_dead = False

    @property
    def is_dead(self):
        return self._is_dead

    @property
    def fitness(self):
        return self._fitness

    @property
    def brain(self):
        return self._brain

    @property
    def length(self):
        return self._length

    def draw(self, frame):
        """
        :param frame: Frame to draw the snake to
        """

        for i in range(self._length):
            if i == 0:
                color = self._head_color
            else:
                color = self._color

            pygame.draw.circle(frame, color, (self._visual_x[i], self._visual_y[i]), Snake.body_radius, 0)

    def move(self, food_pos):
        """
        :param screen_dims: Rightmost and lowermost boundaries (i.e. screen's width and height) in pixels
        :param food_pos:    X and Y coordinates of where the food is

        :return: True if the food has been eaten, False otherwise
        """

        # If hit a boundary, die
        if self._x[0] <= Snake.body_radius or self._x[0] >= Screen.width - Snake.body_radius or \
           self._y[0] <= Snake.body_radius or self._y[0] >= Screen.height - Snake.body_radius:
            self.die()
            return False

        # If hit yourself, also die
        for i in range(1, self._length):
            if self._x[i] - Snake.body_radius / 2 <= self._x[0] <= self._x[i] + Snake.body_radius / 2 and \
               self._y[i] - Snake.body_radius / 2 <= self._y[0] <= self._y[i] + Snake.body_radius / 2:
                self.die()
                return False

        # If the head is on top of food, add a tail and return True
        (food_x, food_y) = food_pos
        if food_x - Snake.body_radius <= self._x[0] <= food_x + Snake.body_radius and \
           food_y - Snake.body_radius <= self._y[0] <= food_y + Snake.body_radius:
            self._directions.append(self._directions[-1])
            self._x.append(self._x[-1] + Snake.body_size * -int(np.cos(np.radians(self._directions[-1]))))
            self._y.append(self._y[-1] + Snake.body_size * -int(np.sin(np.radians(self._directions[-1]))))
            self._visual_x.append(self._x[-1])
            self._visual_y.append(self._y[-1])

            self._length   += 1
            self._velocity += self._velocity * Snake.speedup_rate
            self._starving_lv = 0

            return True

        # If accum has a whole part, move every body part of to the appropriate direction
        if self._accum >= Snake.body_radius:
            self._accum -= Snake.body_radius
            self._timer -= Snake.body_radius

            for i in range(self._length):
                self._x[i] += Snake.body_radius * int(np.cos(np.radians(self._directions[i])))
                self._y[i] += Snake.body_radius * int(np.sin(np.radians(self._directions[i])))
                self._visual_x[i] = self._x[i]
                self._visual_y[i] = self._y[i]

            self._starving_lv += 1
            if self._starving_lv > Snake.max_starving:
                self.die()

            self.set_direction(self._brain.think(self.get_visual_inputs(food_pos)))

        else:   # For smooth movement
            for i in range(self._length):
                self._visual_x[i] += int(self._velocity * np.cos(np.radians(self._directions[i])))
                self._visual_y[i] += int(self._velocity * np.sin(np.radians(self._directions[i])))

        # Time to change direction if needed
        if self._timer <= 0:
            self._directions = [self._next_direction] + self._directions
            del self._directions[-1]

            self._timer += Snake.body_size

        self._accum += self._velocity
        self._lifetime += 1

        return False

    def set_direction(self, direction):
        """
        :param direction: 0 -> up
                          1 -> down
                          2 -> left
                          3 -> right
        """
        assert 0 <= direction <= 3

        if direction == 0 and self._directions[0] != 90 and self._directions[0] != 270:
            self._next_direction = 270
        elif direction == 1 and self._directions[0] != 90 and self._directions[0] != 270:
            self._next_direction = 90
        elif direction == 2 and self._directions[0] != 0 and self._directions[0] != 180:
            self._next_direction = 180
        elif direction == 3 and self._directions[0] != 0 and self._directions[0] != 180:
            self._next_direction = 0

    def mutate(self):
        self._brain.mutate()

    def die(self):
        self._is_dead = True

        # Calculate fitness
        self._fitness = int(np.power(self._lifetime / 200, 2) * np.power(2, self._length))

    def get_visual_inputs(self, food_pos):
        """
        :return A list of 24 integers. Every three elements represent what the snake can see from different directions:
                - The first of the triple contains the distance between its head and the wall
                - The second of the triple contains the distance between its head and the food (if in that direction)
                - The third of the triple contains the distance between its head and its body (if in that direction)

                The snake can see from 8 different angles (relative to the head's current direction) and these will be
                arranged in the following order: [0, 45, 90, 135, 180, 225, 270, 315]
        """
        ret              = []
        (food_x, food_y) = food_pos
        max_distance     = np.maximum(Screen.width, Screen.height)
        multiplier       = -1 / max_distance  # Multiplying this factor by a result and adding one gives range (-1, 1)

        direction = self._directions[0]  # Head's direction
        for i in range(8):
            food_found = False
            body_found = False

            food_dist = -1
            body_dist = -1

            x_incr = Snake.body_size * np.sign(np.round(np.cos(np.radians(direction))))
            y_incr = Snake.body_size * np.sign(np.round(np.sin(np.radians(direction))))

            (x, y) = (self._x[0], self._y[0])
            while 0 < x < Screen.width and 0 < y < Screen.height:
                # If this angle points at food, calculate distance and don't look for food anymore
                if not food_found:
                    if food_x - Snake.body_radius < x < food_x + Snake.body_radius and \
                       food_y - Snake.body_radius < y < food_y + Snake.body_radius:
                        food_dist = int(np.sqrt(pow(self._x[0] - x, 2) + pow(self._y[0] - y, 2)))
                        food_found = True

                # If this angle points at a body part, calculate distance and don't look for body parts anymore
                if not body_found:
                    for j in range(1, self._length):
                        if self._x[j] - Snake.body_radius < x < self._x[j] + Snake.body_radius and \
                           self._y[j] - Snake.body_radius < y < self._y[j] + Snake.body_radius:
                            body_dist = int(np.sqrt(pow(self._x[0] - x, 2) + pow(self._y[0] - y, 2)))
                            body_found = True

                x += x_incr
                y += y_incr

            wall_dist = int(np.sqrt(pow(self._x[0] - x, 2) + pow(self._y[0] - y, 2)))

            ret.append(wall_dist * multiplier + 1)
            ret.append(food_dist * multiplier + 1)
            ret.append(body_dist * multiplier + 1)

            direction += 45

        return ret
