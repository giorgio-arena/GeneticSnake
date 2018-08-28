import numpy as np
import pygame as pg
from screen import Screen


class Snake:
    color   = (0, 0, 0)  # RGB color for the snake's body
    body_sz = 20         # Diameter of each circle (body part)
    speedup = 0.03       # Percentage of velocity gain

    def __init__(self):
        # Positional attributes
        self._x      = [int(Screen.width / 2)]   # List of x coordinates for each of the snake's body parts
        self._y      = [int(Screen.height / 2)]  # List of y coordinates for each of the snake's body parts
        self._length = 1                         # Body length, also equal to the snake's score
        self._colls  = [pg.Rect(self.head_pos(), (Snake.body_sz, Snake.body_sz))]  # Collision boxes for body parts

        # Movement attributes
        self._dirs     = [0]   # Directions for each of the snake's body parts: 0 right, 90 down, 180 left, 270 up
        self._next_dir = 0     # What the head's next direction will be
        self._velocity = 3.0   # How many pixels the snake will travel per frame (added to _accum for each movement)
        self._accum    = 0.0   # Move the snake only visually until < body_sz, then move the actual position by body_sz

        # Flags
        self._is_dead = False

    @property
    def is_dead(self):
        return self._is_dead

    @property
    def length(self):
        return self._length

    def head_pos(self):
        return self._x[0], self._y[0]

    def draw(self, frame):
        """
        :param frame: Frame to draw the snake to
        """

        for i in range(self._length):
            visual_x = int(self._x[i] + self._accum * np.cos(np.radians(self._dirs[i])))
            visual_y = int(self._y[i] + self._accum * np.sin(np.radians(self._dirs[i])))
            pg.draw.circle(frame, Snake.color, (visual_x, visual_y), int(Snake.body_sz / 2), 0)

    def move(self, food_pos):
        """
        :param food_pos: X and Y coordinates of where the food is

        :return: True if the food has been eaten, False otherwise
        """

        # If hit a boundary, die
        if not self._colls[0].colliderect(pg.Rect(Snake.body_sz + 5, Snake.body_sz + 5, Screen.width - Snake.body_sz - 5,
                                                  Screen.height - Snake.body_sz - 5)):
            self.die()
            return False

        # If hit yourself, also die
        for i in range(1, self._length):
            if self._colls[0].contains(self._colls[i]):
                self.die()
                return False

        # If the head is on top of food, add a tail and return True
        if self._colls[0].collidepoint(food_pos):
            self._x.append(self._x[-1] + Snake.body_sz * -int(np.cos(np.radians(self._dirs[-1]))))
            self._y.append(self._y[-1] + Snake.body_sz * -int(np.sin(np.radians(self._dirs[-1]))))
            self._dirs.append(self._dirs[-1])
            self._colls.append(pg.Rect(self._x[-1], self._y[-1], Snake.body_sz, Snake.body_sz))

            self._length   += 1
            self._velocity += self._velocity * Snake.speedup

            return True

        # If accum is got to body_sz, move every body part of to the appropriate direction
        if self._accum >= Snake.body_sz:
            for i in range(self._length):
                self._x[i] += Snake.body_sz * int(np.cos(np.radians(self._dirs[i])))
                self._y[i] += Snake.body_sz * int(np.sin(np.radians(self._dirs[i])))
                self._colls[i] = pg.Rect(self._x[i], self._y[i], Snake.body_sz, Snake.body_sz)

            self._dirs = [self._next_dir] + self._dirs
            del self._dirs[-1]

            self._accum -= Snake.body_sz

        self._accum += self._velocity

        return False

    def set_direction(self, direction):
        """
        :param direction: 0: up, 1: down, 2: left, 3: right
        """
        assert 0 <= direction <= 3

        if direction == 0 and self._dirs[0] != 90 and self._dirs[0] != 270:
            self._next_dir = 270
        elif direction == 1 and self._dirs[0] != 90 and self._dirs[0] != 270:
            self._next_dir = 90
        elif direction == 2 and self._dirs[0] != 0 and self._dirs[0] != 180:
            self._next_dir = 180
        elif direction == 3 and self._dirs[0] != 0 and self._dirs[0] != 180:
            self._next_dir = 0

    def die(self):
        self._is_dead = True
