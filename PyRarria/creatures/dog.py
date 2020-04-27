from PyRarria.creatures.creature import Creature
from PyRarria.creatures.creatures_attributes import DOG, LEFT, RIGHT

import pygame as pg
import random

load = pg.image.load
rand = random.random
randi = random.randint

class Dog(Creature):

    left = [load('img/dogL01.png'), load('img/dogL02.png'),
            load('img/dogL03.png'), load('img/dogL04.png'),
            load('img/dogL05.png'), load('img/dogL06.png'),
            load('img/dogL07.png'), load('img/dogL08.png'),
            load('img/dogL09.png'), load('img/dogL10.png')]

    right = [load('img/dogR01.png'), load('img/dogR02.png'),
             load('img/dogR03.png'), load('img/dogR04.png'),
             load('img/dogR05.png'), load('img/dogR06.png'),
             load('img/dogR07.png'), load('img/dogR08.png'),
             load('img/dogR09.png'), load('img/dogR10.png')]

    frames = 10
    speed = 4

    def __init__(self, x, y):
        self.create(x, y, **DOG)

    def create(self, x, y, w, h, v,
               jump_count, walk_count, hit_count,
               hp, items, attack, defense):

        # position
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = v
        self.hbox = []

        # counters
        self.jump_count = jump_count
        self.walk_count = walk_count
        self.hit_count = hit_count
        self.anime_count = 0

        # boolean
        self.is_left = False
        self.is_right = False
        self.is_jump = False
        self.is_hpbar = False

        # specific for creature
        self.hp = hp
        self.items = items
        self.attack = attack
        self.defense = defense

        # generated in time
        self.steps = 0
        self.direction = 0

    def draw(self, win):

        # TODO sprawdzic czy jeszcze zyje

        self.move(None)

        # creature
        self.anime_count %= self.speed * self.frames
        if self.direction == RIGHT:
            win.blit(self.right[self.anime_count // self.speed], (self.x, self.y))
        else:
            win.blit(self.left[self.anime_count // self.speed], (self.x, self.y))
        self.anime_count += 1

        # hitbox
        self.hitbox = (self.x + self.w * 0.2, self.y + self.h * 0.2,
                       self.w * 0.6, self.h * 0.75)
        pg.draw.rect(win, (255,0,0), self.hitbox, 2)

    def move(self, player):

        # TODO uciekac od gracza

        # during jump
        if self.is_jump:
            if self.jump_count >= 0:
                self.y -= (self.jump_count ** 2) * 0.15
            elif self.jump_count >= -10:
                self.y += (self.jump_count ** 2) * 0.15
            else:
                self.is_jump = False
            self.x += self.direction * self.v
            self.jump_count -= 1


        # maybe jump
        elif not self.is_jump and rand() > 0.99:
            self.is_jump = True
            self.jump_count = 10

        # during move
        elif self.steps > 0:
            self.x += self.direction * self.v
            self.steps -= 1

        # new move
        else:
            self.steps = randi(50,100)
            if rand() > 0.5:
                self.direction = LEFT
            else:
                self.direction = RIGHT

    def hit(self, attack):
        self.is_enemy = True
        self.is_hpbar = True

        # TODO liczyc hp zmiennoprzecinkowo
        self.hp -= int((101 - self.defense) * attack / 101)

    def bite(self, player):
        player.hit(self.attack)

def test():
    dog = Dog(1, 2)
    # print(dir(dog))
    # print(vars(dog))
    print('test OK')
