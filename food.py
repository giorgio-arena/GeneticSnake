import pygame
import random
from screen import Screen
from snake import Snake


def ceil_to_multiple(x, mul):
    return (int(x / mul) + 1) * mul


def get_random_coord(max_coord):
    coord = random.randint(Food.margin, max_coord - Food.margin)
    return ceil_to_multiple(coord, Snake.body_size)


class Food:
    margin = 30

    def __init__(self):
        self._x     = get_random_coord(Screen.width)
        self._y     = get_random_coord(Screen.height)
        self._color = (255, 0, 0);

    def change_pos(self):
        self._x = get_random_coord(Screen.width)
        self._y = get_random_coord(Screen.height)

    def draw(self, frame):
        pygame.draw.circle(frame, self._color, self.dims(), 5, 0)

    def dims(self):
        return self._x, self._y
