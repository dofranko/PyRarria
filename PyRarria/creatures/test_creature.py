import pygame as pg
import random
from PyRarria.creatures.creature import AbstractCreature
from PyRarria.creatures.global_settings import *
from PyRarria.creatures.physical_engine import *
from PyRarria.creatures.vector import PVector


class TestCreature(AbstractCreature):

    def __init__(self, x, y, r):
        super(TestCreature, self).__init__()

        self.radius = r
        self.angle = 0.0
        # self.maxspeed = 2
        # self.maxforce = 0.1

        # GRAVITY TEST
        self.maxspeed = 10
        self.maxforce = 10
        self.mass = 20

        # self.mass = self.radius ** 2
        self.location = PVector(x, y)
        self.velocity = PVector(0, 0)
        self.acceleration = PVector(0, 0)
        self.body = pg.rect.Rect(200, 200, self.radius, self.radius)

    def create(self, **attr):
        pass

    def draw(self, win):
        pg.draw.ellipse(win, (128, 128, 128), self.body)
        pg.draw.ellipse(win, (0, 0, 0), self.body, 5)
        pass

    def hit(self, attack):
        pass

    def bite(self, enemy):
        pass

    def update(self, player):
        self.update_forces(player)
        self.move(player)

    def update_forces(self, player):
        gravity(self)
        friction(self)
        # wind(self)
        edges_ball(self)
        # edges_stop(self)
        # edges(self)

    def move(self, player):
        # fly(self, player)
        # free_fly(self)
        self.velocity += self.acceleration
        self.velocity.limit(self.maxspeed)
        self.location += self.velocity
        self.acceleration *= 0

        self.body.center = self.location.repr()

    def apply_force(self, force):
        force.limit(self.maxforce)
        # f.div(self.mass)
        self.acceleration += force

        # print('force:', force.mag())
        # print('max_force', self.maxforce)

    def collision(self, player):
        pass

    def die(self):
        pass
