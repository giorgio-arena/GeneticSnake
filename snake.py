import pygame
import math
import numpy as np

class Snake:
    def __init__(self):
        # Positional attributes
        self.x = [320]  # List of x coordinates for each of the snake's body parts
        self.y = [240]  # List of y coordinates for each of the snake's body parts

        self.tmp = 0

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

    def get_visual_inputs(self, food_x, food_y):
        """
        :return A list of 24 integers. Every three elements represent what the snake can see from a different angle:
                - The first of the triple will contain the distance between the snake's head and the walls
                - The second of the triple will contain the distance between the snake's head and the food (if present)
                - The third of the triple will contain the distance between the snake's head and its body (if present)

                The snake can see from 8 different angles (relative to the head's current direction) and these will be
                arranged in thhe following order: [0, 45, 90, 135, 180, 225, 270, 315]
        """
        ret = []

        direction = self.directions[0]  # Head's direction
        for i in range(8):
            food_found = False
            body_found = False

            wall_dist = -1
            food_dist = -1
            body_dist = -1

            (x, y) = (self.x[0], self.y[0])
            while 0 < x < 640 and 0 < y < 480:  # TODO: replace raw values
                # If this angle points at food, calculate distance and don't look for food anymore
                if not food_found:
                    if food_x - self.body_size < x < food_x + self.body_size and \
                       food_y - self.body_size < y < food_y + self.body_size:
                        food_dist = int(math.sqrt(pow(self.x[0] - x, 2) + pow(self.y[0] - y, 2)))
                        food_found = True

                # If this angle points at a body part, calculate distance and don't look for body parts anymore
                if not body_found:
                    for j in range(1, len(self.directions)):
                        if self.x[j] - self.body_size < x < self.x[j] + self.body_size and \
                           self.y[j] - self.body_size < y < self.y[j] + self.body_size:
                            body_dist = int(math.sqrt(pow(self.x[0] - x, 2) + pow(self.y[0] - y, 2)))
                            body_found = True

                x += np.sign(np.round(math.cos(math.radians(direction))))
                y += np.sign(np.round(math.sin(math.radians(direction))))

            wall_dist = int(math.sqrt(pow(self.x[0] - x, 2) + pow(self.y[0] - y, 2)))

            ret.append(wall_dist)
            ret.append(food_dist)
            ret.append(body_dist)

            direction += 45

        print(ret[0])

        return ret
