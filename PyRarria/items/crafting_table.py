import pygame
import items.crafting as crafting
from settings import *
from items.placeable import *
from math import hypot

vector = pygame.math.Vector2


class CraftingTable(Placeable):

    STANDARD_RULE_SET = {}
    # TODO change it when table rdy
    STANDARD_RULE_SET["green_sword"] = {"grass": 5, "dirt": 2}
    STANDARD_RULE_SET["black_cat_helmet"] = {"green_sword": 1}

    def __init__(self, x, y, info, game, placed=True):
        super().__init__(x, y, info, game, placed)
        self.is_open = False
        self.use_range = 200
        self.possible_items = []
        self.available_items = []
        self.button_down = False
        self.items_to_draw = pygame.sprite.Group()

    def open(self):
        self.is_open = True
        crafting.add_rule_set(self.STANDARD_RULE_SET)

    def close(self):
        self.is_open = False
        crafting.remove_rule_set(self.STANDARD_RULE_SET)

    def use(self):
        if self.is_open:
            self.close()
        else:
            self.open()

    def update(self):
        super().update()
        if self.is_open and (
            math.hypot(
                self.rect.center[0] - self.game.player.rect.center[0],
                self.rect.center[1] - self.game.player.rect.center[1],
            )
            > self.use_range
        ):
            self.close()
        elif not self.is_open and (
            math.hypot(
                self.rect.center[0] - self.game.player.rect.center[0],
                self.rect.center[1] - self.game.player.rect.center[1],
            )
            <= self.use_range
        ):
            self.open()

    def draw(self):
        super().draw()

    def destroy(self):
        self.close()
        super().destroy()
