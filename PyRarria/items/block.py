import pygame
from settings import *
from items.item import *
from math import sqrt
from os import path


vector = pygame.math.Vector2


class Block(Item):
    def __init__(self, x, y, info, game):
        super().__init__(x, y, info, game)
        self.hp = info.attr["hp"]
        self.stan = 0
        self.max_hp = self.hp
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
        self.dmg_image = None
        self.propability = info.attr["probability"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.range = PLAYER_VALUES["TERRAIN_RANGE"]

    def can_place(self, position):
        if self.game.grid[position]:
            return False
        neighbours = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for n in neighbours:
            if self.game.grid[(BLOCK_SIZE * n[0] + position[0], BLOCK_SIZE * n[1] + position[1])]:
                return True
        return False

    def action(self, mouse_pos, player):
        """places block at cur_pos scaled to range of the player"""
        mouse_pos = vector(mouse_pos[0], mouse_pos[1])
        if math.hypot(mouse_pos.x - player.rect.x, mouse_pos.y - player.rect.y) <= self.range:
            position = vector(player.position.x, player.position.y) + mouse_pos - vector(WIDTH / 2, HEIGHT / 2)
            blok_pos = Item.cursor_to_grid(position.x, position.y)
            if self.can_place(blok_pos):
                self.position = vector(blok_pos)
                self.game.blocks.add(self)
                self.game.grid[(self.position.x, self.position.y)] = self
                return True
        return False

    def update(self):
        super().update()
        if self.hp <= 0:
            self.game.blocks.remove(self)
            self.game.grid[(self.position.x, self.position.y)] = None
            self.skaluj(BLOCK_SIZE // 2)
            self.game.items.add(self)
            return

        stan = 0
        if 1 < self.hp <= self.max_hp / 3:
            stan = 3
        elif self.max_hp / 3 < self.hp <= self.max_hp * (2 / 3):
            stan = 2
        elif self.hp < self.max_hp:
            stan = 1
        if stan == 0:
            return
        if stan != self.stan:
            self.stan = stan
            self.dmg_image = pygame.image.load(IMAGES_LIST[f"damaged_{self.stan}"]).convert_alpha()
            self.dmg_image = pygame.transform.scale(self.dmg_image, (BLOCK_SIZE, BLOCK_SIZE))

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
        if not self.dmg_image:
            return
        self.game.screen.blit(self.dmg_image, self.rect)

    def skaluj(self, rozm):
        """scales image when placed or destroyed"""
        self.image = pygame.transform.scale(self.image, (rozm, rozm))
        X = self.rect.x
        Y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = X
        self.rect.y = Y

    def hit(self, dmg):
        self.hp -= dmg
