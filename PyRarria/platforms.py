# Sprite class for platforms
# ============WATCH OUT========= DO NOT RENAME IT INTO "platform.py" !!!!!!!!!!!!!!
import pygame
from settings import *

vector = pygame.math.Vector2


class Platform(pygame.sprite.Sprite):
    # Standardowo:   ^ position.x, position.y - pozycja względem całej mapy gry
    #               ^ rect.x, rect.y - pozycja względem monitora
    def __init__(self, x, y, width, height, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.position = vector(x, y)
        self.game = game

    # Aktualiacja pozycji platform
    def update(self):
        main_stage_position = self.game.get_main_stage_position()
        self.rect.x = self.position.x + main_stage_position.x
        self.rect.y = self.position.y + main_stage_position.y