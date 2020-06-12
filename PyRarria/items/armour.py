from items.item import Item
import pygame
from settings import *


class Armour(Item):
    """Subclass of Item class. Armour like helmet, breastplate or boots."""

    def __init__(self, x, y, info, game, value):
        super().__init__(x, y, info, game)
        self.delta_y = value
        self.size = 2 / 5

    def activate(self):
        """To implement by subclasses"""

    def deactivate(self):
        """To implement by subclasses"""

    def get_dressed(self):
        """Draw armour on player"""
        rot = self.rot_center(self.image, 0)
        player_width = self.game.player.rect.width
        player_height = self.game.player.rect.height
        if self.game.player.facing == -1:
            rot = pygame.transform.flip(rot, True, False)
        rot = pygame.transform.scale(rot, (player_width, round(player_height * self.size)))
        obr_rect = rot.get_rect()
        obr_rect.x = self.game.player.rect.x
        obr_rect.y = self.game.player.rect.y + self.delta_y * player_height
        self.game.screen.blit(rot, obr_rect)


class Helmet(Armour):
    """Subclass of Armour class."""

    def __init__(self, x, y, info, game):
        super().__init__(x, y, info, game, 0)
        self.defence = info.attr["defence"]
        self.mana_power = info.attr["mana_power"]

    def activate(self):
        PLAYER_VALUES["DEFENCE"] += self.defence
        PLAYER_VALUES["MANA_REDUCTION"] += self.mana_power

    def deactivate(self):
        PLAYER_VALUES["DEFENCE"] -= self.defence
        PLAYER_VALUES["MANA_REDUCTION"] -= self.mana_power


class Breastplate(Armour):
    """Subclass of Armour class."""

    def __init__(self, x, y, info, game):
        super().__init__(x, y, info, game, 1 / 3)
        self.defence = info.attr["defence"]

    def activate(self):
        PLAYER_VALUES["DEFENCE"] += self.defence

    def deactivate(self):
        PLAYER_VALUES["DEFENCE"] -= self.defence


class Boots(Armour):
    """Subclass of Armour class."""

    def __init__(self, x, y, info, game):
        super().__init__(x, y, info, game, 2 / 3)
        self.speed_value = info.attr["speed_value"]
        self.defence = info.attr["defence"]
        self.jump = info.attr["double_jump"]

    def activate(self):
        PLAYER_MOVE["PLAYER_ACC"] += self.speed_value
        PLAYER_VALUES["DEFENCE"] += self.defence
        self.game.player.double_jump = self.jump

    def deactivate(self):
        PLAYER_MOVE["PLAYER_ACC"] -= self.speed_value
        PLAYER_VALUES["DEFENCE"] -= self.defence
        self.game.player.double_jump = False
