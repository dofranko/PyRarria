import pygame as pg

from PyRarria.creatures.vector import PVector


class Arrow(pg.sprite.Sprite):
    def __init__(self):
        super(Arrow, self).__init__()
        self.radius = 10
        self.maxspeed = 10
        self.maxforce = 10
        self.location = PVector(0, 0)
        self.velocity = PVector(0, 0)
        self.acceleration = PVector(0, 0)
        self.body = pg.rect.Rect(200, 200, self.radius, self.radius)

    def draw(self, win):
        pg.draw.ellipse(win, (255, 0, 0), self.body)
        pass

    def update(self):
        self.move()

    def move(self):
        # arrow_fly(self)
        self.velocity += self.acceleration
        self.velocity.limit(self.maxspeed)
        self.location += self.velocity
        self.acceleration *= 0

        self.body.center = self.location.repr()