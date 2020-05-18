import pygame as pg
import random
import math

from PyRarria.creatures.abstract_sprite import AbstractSprite
from PyRarria.creatures.creatures_attributes import *
from PyRarria.creatures.creatures_images import *
from PyRarria.creatures.hp_bar import HpBar
from PyRarria.creatures.physical_engine import *
from PyRarria.creatures.vector import PVector

ANIMATION = BIRD_ANIMATION


class TestCreature(AbstractSprite):

    # static variables
    animation = [ANIMATION['left'], ANIMATION['right']]
    frames = ANIMATION['frames']
    width = ANIMATION['width']
    height = ANIMATION['height']
    radius = min(width, height)
    animation_ticks = math.floor(FPS * ANIMATION['speed'])
    frame_ticks = math.ceil(FPS * ANIMATION['speed'] / ANIMATION['frames'])

    def __init__(self, x, y):
        super(TestCreature, self).__init__(x, y)
        self.create(x, y, **BIRD)

        # GRAVITY TEST
        # self.maxspeed = 10
        # self.maxforce = 10
        # self.mass = 20

        # JUMP TEST
        # self.is_jump = False
        # self.maxspeed = 10
        # self.maxforce = 10
        # self.mass = 20

        # FLY TEST
        # self.manoeuvrability = 0.075
        # self.maxspeed = 3
        # self.maxforce = 5
        # self.mass = 20

        # RUN TEST
        # self.manoeuvrability = 0.02
        # self.maxspeed = 5
        # self.maxforce = 2
        # self.mass = 20

        # TRACK TEST
        # self.manoeuvrability = 0.02
        # self.maxspeed = 5
        # self.maxforce = 5
        # self.mass = 20

        # FLY AFTER
        # self.manoeuvrability = 0.02
        # self.maxspeed = 2
        # self.maxforce = 5
        # self.mass = 20

        # FLY AWAY
        # self.manoeuvrability = 0.02
        # self.maxspeed = 2
        # self.maxforce = 5
        # self.mass = 20

        # RUN AWAY
        # self.manoeuvrability = 0.02
        # self.maxspeed = 3
        # self.maxforce = 5
        # self.mass = 20

    def create(self, x, y, manoeuvrability, maxspeed, maxforce, maxhp,
               mass, items, damage, defense):

        # variables
        self.radius = min(self.width, self.height)
        self.angle = 0.0
        self.mass = mass

        # limits
        self.maxspeed = maxspeed
        self.maxforce = 10
        self.maxhp = maxhp
        self.manoeuvrability = manoeuvrability

        # flags
        self.is_enemy = True
        self.is_hpbar = True
        self.is_hitbox = True
        self.is_fixpos = True

        # counters
        self.anim_count = 0
        self.bite_count = 0
        self.shot_count = 0

        # vectors
        self.location = PVector(x, y)
        self.velocity = PVector(0, 0.001)
        self.acceleration = PVector(0, 0)

        # body
        w, h = self.width, self.height
        self.rect = pg.rect.Rect(0, 0, w, h)
        self.rect.center = self.location.repr()
        self.body = pg.rect.Rect(self.rect)
        self.hpbar = HpBar(self.body.midtop)

        # sprite specific
        self.hp = maxhp
        self.items = items
        self.damage = damage
        self.defense = defense

        # SHOT TEST
        # self.maxforce = 10
        # self.maxspeed = 10

    def draw(self, win):
        # body
        # frame = self.anim_count // self.frame_ticks
        # direction = self.velocity.anim_direction()
        # win.blit(self.animation[direction][frame], self.body)

        # TEST ROTATE BODY
        frame = self.anim_count // self.frame_ticks
        direction = self.velocity.anim_direction()
        image = pg.transform.rotate(
            self.animation[direction][frame],
            -self.velocity.angle_deg())
        win.blit(image, self.body)

        # hitbox
        # TODO, moze sie roznic od obrazka
        if self.is_hitbox:
            pg.draw.rect(win, (255, 0, 0), self.rect, 2)

        # hpbar
        if self.is_hpbar:
            self.hpbar.draw(win, self.hp, self.maxhp)

    def hit(self, weapon):
        if pg.sprite.collide_rect(self, weapon):
            self.is_enemy = True
            self.is_hpbar = True

            self.hp -= (101 - self.defense) * weapon.damage / 101
            print(self.hp)

    def bite(self, player):
        if self.is_enemy and self.rect.colliderect(player):
            if self.bite_count > 0:
                self.bite_count -= 1
            else:
                player.hit(self.damage)
                self.bite_count = 10

    def update(self, player, platforms):
        # dead
        if self.hp <= 0:
            self.die()
            return

        # alive
        self.update_forces(player, platforms)
        self.move(player)

    def update_forces(self, player, platforms):
        # if self.shot_count == 0:
        #     shoot(self, self.location, player.location)
        #     self.shot_count = 10

        # fly(self)
        # run(self)
        # run_away(self, player)
        # gravity(self)
        # run_after(self, player)
        # track(self, player)
        # fly_after(self, player)
        # fly_away(self, player)
        # if self.velocity.y == 0:
        init_move(self)

        gravity(self)
        # keep_on_platform(self, platforms)
        # push_from_platform(self, platforms)
        jump_from_platform(self, platforms)
        # friction(self)
        # wind(self)
        edges_ball(self)
        # edges_stop(self)
        # edges(self)

    def move(self, player):
        # move
        self.velocity += self.acceleration
        self.velocity.limit(self.maxspeed)
        self.location += self.velocity
        self.acceleration *= 0

        # update body
        self.body.center = self.location.repr()
        self.rect.center = self.location.repr()
        self.hpbar.center(self.body.midtop)

        # update animation counter
        self.anim_count += 1
        self.anim_count %= self.animation_ticks

    def apply_force(self, force):
        force.limit(self.maxforce)
        self.acceleration += force

    def die(self):
        self.kill()
