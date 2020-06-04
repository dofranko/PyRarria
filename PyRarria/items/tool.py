import pygame
from settings import *
from items.item import Item


class Tool(Item):
    """Subclass of Item class. Tools like axe or hammer"""

    def __init__(self, x, y, name, game, durability=30):
        super().__init__(x, y, name, game)
        self.durability = durability

    def action(self):
        self.durability -= 1
        if self.durability <= 0:
            return True
        return False
