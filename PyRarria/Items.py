import pygame
from os import path
from settings import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, info, game):
        pygame.sprite.Sprite.__init__(self)

        self.name = info.name
        self.description = info.description

        self.image = pygame.image.load(path.join(IMAGES, info.zdj))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.pos_x = x
        self.pos_y = y

        self.vel_y = 0
        self.acc_y = 0

        self.angle = info.angle

        self.game = game

    def check_collision(self):
        if self.vel_y > 0:
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)

            if hits:
                self.pos_y = min([(hits[i].position.y - self.rect.height) for i in range(len(hits))])
                self.vel_y = 0

    def spadanie(self):
        self.check_collision()
        self.acc_y = PLAYER_GRAV
        self.vel_y += self.acc_y
        if self.vel_y != 0:
            self.pos_y += self.vel_y + 0.5 * self.acc_y

    def get_state(self):
        if self == self.game.player.trzymany:
            return 'trzymany'
        if self in self.game.items:
            return 'lezacy'
        return 'eq'

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def update(self):
        main_stage_pos = self.game.get_main_stage_position()
        self.rect.x = self.pos_x + main_stage_pos.x
        self.rect.y = self.pos_y + main_stage_pos.y

        if self.get_state() == 'lezacy':
            self.spadanie()

    # tylko dla itemu trzymanego przez playera
    def draw(self):
        obr = self.rot_center(self.image, self.angle)
        if self.game.player.facing == -1:
            obr = pygame.transform.flip(obr, True, False)
        obr_rect = obr.get_rect()
        obr_rect.x = self.game.player.rect.x
        obr_rect.y = self.game.player.rect.y
        self.game.screen.blit(obr, obr_rect)

    # implementowane przez podklasy
    def akcja(self):
        pass