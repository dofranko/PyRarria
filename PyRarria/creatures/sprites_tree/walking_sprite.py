from creatures.physical_engine import *
from creatures.sprites_tree.sprite import Sprite
import pygame as pg


class WalkingSprite(Sprite):
    def draw(self, win):
        # body
        frame = self.anim_count // self.frame_ticks
        direction = self.velocity.anim_direction()
        win.blit(self.animation[direction][frame], self.body)

        # hitbox
        # TODO, moze sie roznic od obrazka
        if self.is_hitbox:
            pg.draw.rect(win, (0, 0, 255), self.rect, 2)

        # hpbar
        if self.is_hpbar:
            self.hpbar.draw(win, self.hp, self.maxhp)

    def update_forces(self, player, blocks):
        if self.is_hpbar:
            run_away(self, player)
        else:
            run(self)
        gravity(self)
        keep_on_platform(self, blocks)
        freeze(self)
        player_delete(self, player)
