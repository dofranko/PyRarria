import pygame
from settings import *
from items.item import *


class Food(Item):
    """Subclass of Item class. Just food, y'a know"""

    def __init__(self, x, y, name, game, health_points=20):
        super().__init__(x, y, name, game)
        self.health_points = health_points

    def action(self):
        return self.game.player.heal(self.health_points)
