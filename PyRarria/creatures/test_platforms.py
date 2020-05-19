import pygame as pg


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.rect.Rect(x, y, w, h)

    def draw(self, win):
        pg.draw.rect(win, (0, 255, 0), self.rect)