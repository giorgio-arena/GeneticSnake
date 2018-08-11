import pygame
import random
from screen import Screen
from snake import Snake


def ceil_to_multiple(x, mul):
    return (int(x / mul) + 1) * mul


class Food:
    margin = 30

    def __init__(self):
        self.x     = ceil_to_multiple(random.randint(Food.margin, Screen.width - Food.margin), Snake.body_size)
        self.y     = ceil_to_multiple(random.randint(Food.margin, Screen.height - Food.margin), Snake.body_size)
        self.color = (255, 0, 0);

    def change_pos(self):
        self.x = ceil_to_multiple(random.randint(Food.margin, Screen.width - Food.margin), Snake.body_size)
        self.y = ceil_to_multiple(random.randint(Food.margin, Screen.height - Food.margin), Snake.body_size)

    def draw(self, frame):
        pygame.draw.circle(frame, self.color, self.dims(), 5, 0)

    def dims(self):
        return self.x, self.y
