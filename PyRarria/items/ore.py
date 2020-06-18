import pygame
from settings import *
from items.item import *
from math import sqrt
from os import path
from items_factory import *
import random

vector = pygame.math.Vector2


class Ore(Block):
    def __init__(self, x, y, info, game, placed=True):
        super().__init__(x, y, info, game, placed)

    def update(self):
        super().update()

    def destroy(self):
        self.game.grid[(self.position.x, self.position.y)] = None
        if random.random() < self.propability:
            self.game.items.add(
                self.game.items_factory.create(BLOCKS_ASSOCIATION_LIST[self.name], self.position.x, self.position.y)
            )
        self.kill()
        return
