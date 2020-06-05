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
        self.rng = info.attr["range"]

    def action(self, mouse_pos, player):
        if math.hypot(mouse_pos[0] - player.rect.x, mouse_pos[1] - player.rect.y) <= self.rng:
            damaged = False
            for creature in self.game.all_creatures:
                if creature.rect.collidepoint(mouse_pos):
                    creature.hit(self.damage)
                    damaged = True
                    break
            else:
                for platform in self.game.platforms:
                    if platform.rect.collidepoint(mouse_pos):
                        # platform.hit(self.damage)
                        damaged = True
                        break
            if damaged:
                self.durability -= 1
                print("tak")
            if self.durability <= 0:
                return True
        return False
