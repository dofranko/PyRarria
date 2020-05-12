# Sprite class for platforms
#============WATCH OUT========= DO NOT RENAME IT INTO "platform.py" !!!!!!!!!!!!!!
import pygame
from settings import *
vec = pygame.math.Vector2

class Platform(pygame.sprite.Sprite):
    #Standardowo:   ^ pos.x, pos.y - pozycja względem całej mapy gry
    #               ^ rect.x, rect.y - pozycja względem monitora
    def __init__(self, x, y, width, height, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)
        self.game = game
    
    #Aktualiacja pozycji platform
    def update(self):
        main_stage_pos = self.game.get_main_stage_pos()
        self.rect.x = self.pos.x + main_stage_pos.x
        self.rect.y = self.pos.y + main_stage_pos.y