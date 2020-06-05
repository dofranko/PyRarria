import pygame
from settings import *
from items.item import *


class Food(Item):
    """Subclass of Item class. Just food, y'a know"""

    def __init__(self, x, y, info, game):
        super().__init__(x, y, info, game)
        self.health_points = info.attr["health_points"]

    def action(self, *args):
        return self.game.player.heal(self.health_points)
