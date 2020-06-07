from creatures.physical_engine import *
from creatures.sprites_tree.sprite import Sprite
import pygame as pg


class FlyingSprite(Sprite):
    def draw(self, win):
        # rotate body
        frame = self.anim_count // self.frame_ticks
        direction = self.velocity.anim_direction()
        image = pg.transform.rotate(self.animation[direction][frame], -self.velocity.angle_deg())
        win.blit(image, self.body)

        # hitbox
        # TODO, moze sie roznic od obrazka
        if self.is_hitbox:
            pg.draw.rect(win, (0, 0, 255), self.rect, 2)

        # hpbar
        if self.is_hpbar:
            self.hpbar.draw(win, self.hp, self.maxhp)

    def update_forces(self, player, blocks):
        fly(self)
        edges_bounce(self)
        bounce_from_platform(self, platforms)
        freeze(self)
