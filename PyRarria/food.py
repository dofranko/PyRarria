import pygame
from settings import *
from items import *


class Food(Item):
    """Subclass of Item class. Just food, y'a know"""

    def __init__(self, x, y, name, game):
        super().__init__(x, y, name, game)

    def akcja(self):
        pass
