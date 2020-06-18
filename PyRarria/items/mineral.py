import pygame
from settings import *
from items.item import *


class Mineral(Item):
    """Subclass of Cr class. Crystals"""

    def __init__(self, x, y, info, game):
        super().__init__(x, y, info, game)
