import pygame
import math


class Snake:
    def __init__(self):
        # Positional attributes
        self.x = [320]  # List of x coordinates for each of the snake's body parts
        self.y = [240]  # List of y coordinates for each of the snake's body parts

        # Movement attributes
        self.directions     = [0]   # Directions for each of the snake's body parts: 0 right, 90 down, 180 left, 270 up
        self.next_direction = 0     # What the head's next direction will be
        self.velocity       = 0.2   # How many pixels the snake will travel per frame (1 is maximum)
        self.speedup_rate   = 0.03  # Percentage of velocity gain
        self.accum          = 0.0   # Don't move the snake until < 1, then move by and subtract 1

        # Snake's look
        self.body_size = 10         # Radius of each circle (body part)
        self.color     = (0, 0, 0)  # RGB color for the snake's body

        # Frames before moving to a next direction
        self.timer = self.body_size * 2

        # Flags
        self.dead = False

    def draw(self, frame):
        """
        :param frame: Frame to draw the snake to
        """

        for i in range(len(self.directions)):
            pygame.draw.circle(frame, self.color, (self.x[i], self.y[i]), self.body_size, 0)

    def move(self, width, height, food_pos):
        """
        :param width:    Rightmost boundary (i.e. screen's width) in pixels
        :param height:   Lowermost boundary (i.e. screen's height) in pixels
        :param food_pos: X and Y coordinates of where the food is

        :return: True if the food has been eaten, False otherwise
        """

        # If hit a boundary, die
        if self.x[0] <= self.body_size or self.x[0] >= width - self.body_size or \
           self.y[0] <= self.body_size or self.y[0] >= height - self.body_size:
            self.die()
            return False

        # If hit yourself, also die
        for i in range(1, len(self.directions)):
            if self.x[i] - self.body_size / 2 <= self.x[0] <= self.x[i] + self.body_size / 2 and \
               self.y[i] - self.body_size / 2 <= self.y[0] <= self.y[i] + self.body_size / 2:
                self.die()
                return False

        # If the head is on top of food, add a tail and return True
        (food_x, food_y) = food_pos
        if food_x - self.body_size <= self.x[0] <= food_x + self.body_size and \
           food_y - self.body_size <= self.y[0] <= food_y + self.body_size:
            self.has_eaten = True

            self.directions.append(self.directions[-1])
            self.x.append(self.x[-1] + self.body_size * 2 * -int(math.cos(math.radians(self.directions[-1]))))
            self.y.append(self.y[-1] + self.body_size * 2 * -int(math.sin(math.radians(self.directions[-1]))))

            self.velocity += self.velocity * self.speedup_rate

            return True

        # If accum has a whole part, move every body part of to the appropriate direction
        if self.accum >= 1:
            self.accum -= 1
            self.timer -= 1

            for i in range(len(self.directions)):
                self.x[i] += int(math.cos(math.radians(self.directions[i])))
                self.y[i] += int(math.sin(math.radians(self.directions[i])))

        # Time to change direction if needed
        if self.timer <= 0:
            self.directions = [self.next_direction] + self.directions
            del self.directions[-1]

            self.timer += self.body_size * 2

        self.accum += self.velocity

        return False

    def set_direction(self, direction):
        """
        :param direction: ["up" | "down" | "left" | "right"]
        """

        if direction == "up" and self.directions[0] != 90 and self.directions[0] != 270:
            self.next_direction = 270
        elif direction == "down" and self.directions[0] != 90 and self.directions[0] != 270:
            self.next_direction = 90
        elif direction == "left" and self.directions[0] != 0 and self.directions[0] != 180:
            self.next_direction = 180
        elif direction == "right" and self.directions[0] != 0 and self.directions[0] != 180:
            self.next_direction = 0

    def die(self):
        self.dead = True

    def is_dead(self):
        return self.dead
