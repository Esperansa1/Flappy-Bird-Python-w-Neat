import pygame

BLACK = (0, 0, 0)


class Pillar():
    def __init__(self, screen: pygame.Surface, x, y):
        self.screen = screen
        self.gap = 100
        self.x = x
        self.y = y
        self.top = self.y - self.gap
        self.bottom = self.y + self.gap

    def draw(self):
        pygame.draw.rect(self.screen, BLACK,
                         (self.x, self.y+self.gap, 50, 1000))
        pygame.draw.rect(self.screen, BLACK, (self.x, 0, 50, self.y-self.gap))
