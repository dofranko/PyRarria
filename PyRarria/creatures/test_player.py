import pygame as pg
from pygame.rect import Rect

from creatures.vector import PVector

walk_right = [
    pg.image.load("images/R1.png"),
    pg.image.load("images/R2.png"),
    pg.image.load("images/R3.png"),
    pg.image.load("images/R4.png"),
    pg.image.load("images/R5.png"),
    pg.image.load("images/R6.png"),
    pg.image.load("images/R5.png"),
    pg.image.load("images/R6.png"),
    pg.image.load("images/R7.png"),
]


walk_left = [
    pg.image.load("images/L1.png"),
    pg.image.load("images/L2.png"),
    pg.image.load("images/L3.png"),
    pg.image.load("images/L4.png"),
    pg.image.load("images/L5.png"),
    pg.image.load("images/L6.png"),
    pg.image.load("images/L5.png"),
    pg.image.load("images/L6.png"),
    pg.image.load("images/L7.png"),
]


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.v = 5
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.rect = Rect(self.x + 20, self.y, 28, 60)
        self.hp = 100
        self.location = PVector(x, y)
        self.damage = 1

    def draw(self, win):
        self.x = self.location.x - self.width // 2
        self.y = self.location.y - self.height // 2

        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if not self.standing:
            if self.left:
                win.blit(walk_left[self.walk_count // 3], (int(self.x), int(self.y)))
                self.walk_count += 1
            elif self.right:
                win.blit(walk_right[self.walk_count // 3], (int(self.x), int(self.y)))
                self.walk_count += 1
        else:
            if self.right:
                win.blit(walk_right[0], (int(self.x), int(self.y)))
            else:
                win.blit(walk_left[0], (int(self.x), int(self.y)))
        self.rect = Rect(self.x + 17, self.y + 11, 29, 52)
        pg.draw.rect(win, (255, 0, 0), self.rect, 2)

    def hit(self, attack):
        self.hp -= attack
        print(self.hp)
        # self.jump = False
        # self.jump_count = 10
        # self.x = 60
        # self.y = 410
        # self.walk_count = 0
        # font1 = pg.font.SysFont('comicsans', 100)
        # text = font1.render('-5', 1, (255,0,0))
        # win.blit(text, (250 - text.get_width()//2, 200))
        # pg.display.update()
        # i = 0
        # while i < 300:
        #     pg.time.delay(10)
        #     i += 1
        #     for event in pg.event.get():
        #         if event.type == pg.QUIT:
        #             i = 301
        #             pg.quit()
