from pygame.rect import Rect


WIDTH = 50
HEIGHT = 20
GREY = (105, 105, 105)
GREEN = (0, 255, 0)


class HpBar(object):
    def __init__(self, midtop):
        self.outer = Rect(0, 0, WIDTH, HEIGHT)
        self.inner = Rect(0, 0, WIDTH - 2, HEIGHT - 2)
        self.inner.center = (midtop[0], midtop[1] - 15)
        self.outer.center = (midtop[0], midtop[1] - 15)

    def center(self, midtop):
        self.outer.center = (midtop[0], midtop[1] - 15)
        self.inner.topleft = self.outer.x + 1, self.outer.y + 1

    def draw(self, win, curr_hp, max_hp):
        self.inner.width = ((WIDTH - 2) * curr_hp) // max_hp
        win.fill(GREY, self.outer)
        win.fill(GREEN, self.inner)
