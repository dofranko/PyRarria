from PyRarria.creatures.creature import AbstractCreature
from PyRarria.creatures.creatures_attributes import DOG
from PyRarria.creatures.creatures_attributes import LEFT, RIGHT

from PyRarria.creatures.creatures_images import *
from PyRarria.creatures.global_settings import *
from PyRarria.creatures.hp_bar import HpBar

from pygame.rect import Rect
import pygame as pg
import random

rand = random.random
randi = random.randint


class Dog(AbstractCreature):

    animation = [DOG_LEFT, DOG_RIGHT]
    frames = DOG_FRAMES
    speed = 4

    def __init__(self, x, y):
        super(Dog, self).__init__()
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
        self.rect = Rect(x, y, 0.8*w, 0.8*h)
        self.hpbar = HpBar(x, y, w, h)

        # counters
        self.jump_count = 0
        self.walk_count = 0
        self.bite_count = 0
        self.anim_count = 0

        # timers
        self.jump_timer = jump_timer
        self.walk_timer = walk_timer
        self.bite_timer = bite_timer
        self.anim_timer = anim_timer

        # flags
        self.is_left = False
        self.is_right = False
        self.is_stand = False
        self.is_enemy = True
        self.is_jump = False
        self.is_hpbar = True
        self.is_hitbox = True
        self.is_fixpos = True

        # specific for creature
        self.curr_hp = hp
        self.max_hp = hp
        self.items = items
        self.damage = damage
        self.defense = defense

        # generated in time
        self.direction = 0

    def update(self, player):
        # dead
        if self.curr_hp <= 0:
            self.die()
            return

        # still alive
        self.collision(player)
        self.move(player)

        # update animation
        self.anim_count += 1
        self.anim_count %= self.speed * self.frames

    def draw(self, win):
        x = self.x
        y = self.y
        direction = self.direction

        # main frame
        if self.is_stand:
            win.blit(self.animation[direction][0], (x, y))

        else:
            frame = self.anim_count // self.speed
            win.blit(self.animation[direction][frame], (x, y))

        # hitbox
        if self.is_hitbox:
            pg.draw.rect(win, (255, 0, 0), self.rect, 2)

        # hbbar
        if self.is_hpbar:
            self.hpbar.draw(win, self.curr_hp, self.max_hp)

    def move(self, player):
        # during stand
        if self.is_stand:
            if self.walk_count >= 0:
                pass
            else:
                self.is_stand = False
            self.walk_count -= 1

        # during move
        elif self.walk_count > 0:
            self.x += self.direction * self.v
            self.walk_count -= 1

        # new move or stand
        else:
            self.walk_count = randi(80, 120)

            if rand() > 0.5:
                self.is_stand = True

            if rand() > 0.5:
                self.direction = LEFT
            else:
                self.direction = RIGHT

        # fix position
        if self.is_fixpos:
            if self.x < 0:
                self.x = 0
            elif self.x > SCREEN_WIDTH - self.w:
                self.x = SCREEN_WIDTH - self.w

        # update hitbox
        self.rect.centerx = self.x + self.w//2
        self.rect.centery = self.y + self.h//2

        # update hpbar
        self.hpbar.move(self.x, self.y, self.w, self.h)

    def hit(self, weapon):
        if pg.sprite.collide_rect(self, weapon):
            self.is_enemy = True
            self.is_hpbar = True

            self.curr_hp -= (101 - self.defense) * weapon.damage / 101
            print(self.curr_hp)

    def bite(self, player):
        if not self.is_enemy:
            pass
        elif self.bite_count > 0:
            self.bite_count -= 1
        else:
            player.hit(self.damage)
            self.bite_count = self.bite_timer

    def collision(self, player):
        if self.is_enemy and pg.sprite.collide_rect(self, player):
            self.bite(player)

    def die(self):
        print("Dog is dead!")
        self.kill()


def test():
    # dog = Dog(1, 2)
    # print(dir(dog))
    # print(vars(dog))
    print('test OK')
