from pygame.rect import Rect

INNER_WIDTH = 98
OUTER_WIDTH = 100
INNER_HEIGHT = 18
OUTER_HEIGHT = 20
GREY = (105,105,105)
GREEN = (0, 255, 0)


class HpBar(object):
    def __init__(self, x, y, w, h):
        self.inner = Rect(0, 0, INNER_WIDTH, INNER_HEIGHT)
        self.outer = Rect(0, 0, OUTER_WIDTH, OUTER_HEIGHT)
        self.inner.center = (x+w//2, y+h//2)
        self.outer.center = (x+w//2, y+h//2)

    def move(self, x, y, w, h):
        self.outer.center = (x + w//2, y)
        self.inner.topleft = self.outer.x + 1, self.outer.y + 1

    def draw(self, win, curr_hp, max_hp):
        self.inner.width = (INNER_WIDTH * curr_hp) // max_hp
        win.fill(GREY, self.outer)
        win.fill(GREEN, self.inner)
