from random import randint
from Pillar import Pillar


class PillarManager():
    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen

        self.width = WIDTH
        self.height = HEIGHT

        self.pillars = []
        self.spawn_pillars()

    def spawn_pillars(self):
        pillar_x = 400
        for i in range(4):
            pillar_y = randint(self.height //
                               4, self.height - self.height // 3)
            pillar = Pillar(self.screen, pillar_x, pillar_y)
            self.pillars.append(pillar)
            pillar_x += 200

    def move_pillars(self):

        for pillar in self.pillars:
            if pillar.x < -50:
                pillar.x += self.width+50
                pillar.y = randint(
                    self.height // 4, self.height - self.height // 4)
                pillar.top = pillar.y - pillar.gap
                pillar.bottom = pillar.y + pillar.gap

            pillar.x -= 2

    def draw_pillars(self):
        for pillar in self.pillars:
            pillar.draw()

    def restart_pillars(self):
        self.pillars = []
        self.spawn_pillars()
