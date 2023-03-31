import pygame
from random import randint
BLACK = (0, 0, 0)


class Bird():
    def __init__(self, screen: pygame.Surface, pos, brain, genome):
        self.pos = pos
        self.screen = screen
        self.y_velocity = 4
        self.brain = brain
        self.genome = genome
        self.x, self.y = self.pos
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

    def flap(self):
        self.y_velocity = -6

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.pos, 20)

    def move(self):

        if self.y_velocity <= 6:
            self.y_velocity += 0.3
        self.y += self.y_velocity
        self.pos = (self.x, self.y)
