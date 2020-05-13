import pygame as pg
from pygame.rect import Rect
from pygame.sprite import Sprite


class Weapon(Sprite):

    def __init__(self, x, y, w, h):
        super(Weapon, self).__init__()
        self.damage = 1
        self.rect = Rect(x, y, w, h)

    def move(self, pos):
        self.rect.center = pos

    def draw(self, win):
        pg.draw.rect(win, (255, 0, 0), self.rect, 2)

    def hit(self, damage):
        pass
