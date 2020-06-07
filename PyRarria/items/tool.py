import pygame
import math
from settings import *
from items.item import Item


class Tool(Item):
    """Subclass of Item class. Tools like axe or hammer"""

    def __init__(self, x, y, info, game):
        super().__init__(x, y, info, game)
        self.durability = info.attr["durability"]
        self.damage = info.attr["damage"]
        self.range = info.attr["range"]
        self.env_damage = info.attr["env_damage"]
