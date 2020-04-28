from PyRarria.creatures.creature import Creature
from PyRarria.creatures.creatures_attributes import DOG
from PyRarria.creatures.creatures_attributes import LEFT, RIGHT, DEAD, ALIVE
from PyRarria.settings import *

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
               jump_timer, walk_timer, bite_timer, anim_timer,
               hp, items, damage, defense):

        # position
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = v
        self.hbox = (0, 0, 0, 0)

        # counters
        self.jump_count = 0
        self.walk_count = 0
        self.bite_count = 0
        self.anim_count = 0
        self.temp_count = 0

        # timers
        self.jump_timer = jump_timer
        self.walk_timer = walk_timer
        self.bite_timer = bite_timer
        self.anim_timer = anim_timer

        # flags
        self.is_left = False
        self.is_right = False
        self.is_enemy = True
        self.is_jump = False
        self.is_hpbar = False

        # specific for creature
        self.hp = hp
        self.items = items
        self.damage = damage
        self.defense = defense

        # generated in time
        self.steps = 0
        self.direction = 0

    def draw(self, win, player):

        # hitbox
        self.hbox = (self.x + self.w * 0.2,
                     self.y + self.h * 0.2,
                     self.w * 0.6, self.h * 0.75)
        pg.draw.rect(win, (255,0,0), self.hbox, 2)

        # TODO sprawdzic czy jeszcze zyje
        if self.hp <= 0:
            return DEAD

        self.collision(player)
        # self.move(player)

        # creature
        self.anim_count %= self.speed * self.frames
        if self.direction == RIGHT:
            win.blit(self.right[self.anim_count // self.speed], (self.x, self.y))
        else:
            win.blit(self.left[self.anim_count // self.speed], (self.x, self.y))
        self.anim_count += 1

        # hbbar
        if self.is_hpbar:
            hpbar_out = (self.hbox[0], self.hbox[1] - 30,
                         self.hbox[2], 15)
            hpbar_in = (self.hbox[0] + 1, self.hbox[1] - 29,
                        (self.hbox[2] - 2) * self.hp/100, 13)
            win.fill(GREY, hpbar_out)
            win.fill(GREEN, hpbar_in)

        return ALIVE

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

    def hit(self, weapon):
        if (
            weapon.hbox[0] < self.hbox[0] + self.hbox[2] and
            weapon.hbox[0] + weapon.hbox[2] > self.hbox[0] and
            weapon.hbox[1] < self.hbox[1] + self.hbox[3] and
            weapon.hbox[1] + weapon.hbox[3] > self.hbox[1]
        ):
            self.is_enemy = True
            self.is_hpbar = True

            self.hp -= (101 - self.defense) * weapon.damage / 101
            print(self.hp)

    def bite(self, player):
        if self.bite_count > 0:
            self.bite_count -= 1
        else:
            player.hit(self.damage)
            self.bite_count = self.bite_timer

    def collision(self, player):
        if self.is_enemy and (
            player.hbox[0] < self.hbox[0] + self.hbox[2] and
            player.hbox[0] + player.hbox[2] > self.hbox[0] and
            player.hbox[1] < self.hbox[1] + self.hbox[3] and
            player.hbox[1] + player.hbox[3] > self.hbox[1]
        ):
            self.bite(player)

    def die(self):
        print("Dog is dead!")
        pass

def test():
    dog = Dog(1, 2)
    # print(dir(dog))
    # print(vars(dog))
    print('test OK')
