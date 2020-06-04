import pygame
from settings import *
from items import *


class Tool(Item):
    """Subclass of Item class. Tools like axe or hammer"""

    def __init__(self, x, y, name, game):
        super().__init__(x, y, name, game)

    def akcja(self):
        pass
