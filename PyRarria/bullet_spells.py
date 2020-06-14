import pygame
import random
from settings import *
from spritesheet import *
from items.item import *


SPELL_SPEED = {
    "fireball": 3,
    "frostbullet": 3,
}


class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.sheet = SpriteSheet(SPELL_SHEETS["collision_explosion"], 10, 6, 60)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.position = pos + (self.sheet.shift[4][0], self.sheet.shift[4][1])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.start = pygame.time.get_ticks()
        self.frame = 0

    # Rysowanie kolejnej klatki tego efektu
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index])
        self.frame += 1

    # Sprawdzanie czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        if self.frame == 56:
            self.kill()

        self.draw(self.frame)
        main_stage_position = self.game.get_main_stage_position()
        self.rect.x = self.position.x + main_stage_position.x
        self.rect.y = self.position.y + main_stage_position.y


class BulletSpell(pygame.sprite.Sprite):
    """Super class for spells"""

    def __init__(self, game, pos, name, damage, speed_y, direction):
        self.groups = game.magics
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.position = pos
        self.damage = damage + PLAYER_VALUES["DAMAGE"]
        self.speed_y = speed_y
        self.start = pygame.time.get_ticks()
        self.direction = direction

    def check_collision(self):
        """Check collision with creatures and environment"""
        hits = pygame.sprite.spritecollide(self, self.game.all_creatures, False)
        if hits:
            for hit in hits:
                hit.hit(self, self.damage)
            self.explode()

        hits = pygame.sprite.spritecollide(self, Item.get_neighbours(self.position, (5, 5), self.game.grid), False)
        if hits:
            self.explode()

    def explode(self):
        """Make explosion after colliding with object (should override)"""
        self.kill()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.start > self.duration:
            self.kill()

        main_stage_position = self.game.get_main_stage_position()
        self.rect.x = self.position.x + main_stage_position.x
        self.rect.x += self.speed_x * self.direction
        self.rect.y = self.position.y + main_stage_position.y
        self.rect.y += self.speed_y
        self.position.y += self.speed_y
        self.position.x += self.speed_x * self.direction

        self.draw(self.frame)
        self.check_collision()


# Klasa zaklęcia fireball, czyli lecący ognisty pocisk
class FireBall(BulletSpell):
    def __init__(self, game, pos, speed_y, direction):
        super().__init__(game, pos, "fireball", SPELL_VALUE["fireball"], speed_y, direction)
        if direction == 1:
            self.sheet = SpriteSheet(SPELL_SHEETS["fireball_right"], 8, 8, 64)
        else:
            self.sheet = SpriteSheet(SPELL_SHEETS["fireball_left"], 8, 8, 64)

        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.frame = random.randint(0, 63)
        self.rect = self.image.get_rect()
        self.speed_x = SPELL_SPEED["fireball"]
        self.duration = SPELL_DURATION["fireball"]

    # Rysowanie kolejnej klatki tego efektu
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[int(cell_index)])
        self.frame += 1

    # Sprawdzanie czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        if self.frame == 64:
            self.frame = 0
        super().update()

    def explode(self):
        vect = pygame.math.Vector2(self.position.x, self.position.y)
        if self.direction == 1:
            vector = pygame.math.Vector2(self.position[0] + 50, self.position[1] + 10)
            new_explosion = Explosion(self.game, vector)
        else:
            vector = pygame.math.Vector2(self.position[0], self.position[1] + 10)
            new_explosion = Explosion(self.game, vector)

        self.game.explosions.add(new_explosion)
        self.kill()


# Klasa zaklęcia frostbullet, czyli lecący lodowy pocisk
class FrostBullet(BulletSpell):
    def __init__(self, game, pos, speed_y, direction):
        super().__init__(game, pos, "frostbullet", SPELL_VALUE["frostbullet"], speed_y, direction)
        if direction == 1:
            self.sheet = SpriteSheet(SPELL_SHEETS["frostbullet_right"], 8, 1, 8)
        else:
            self.sheet = SpriteSheet(SPELL_SHEETS["frostbullet_left"], 8, 1, 8)

        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed_x = SPELL_SPEED["frostbullet"]
        self.duration = SPELL_DURATION["frostbullet"]
        self.frame = 0

    # Rysowanie kolejnej klatki tego efektu
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[int(cell_index)])
        self.frame += 1

    # Sprawdzanie, czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        if self.frame == 8:
            self.frame = 0
        super().update()

    def explode(self):
        self.game.creatures_engine.freeze(
            self.position, SPELL_DURATION["frostbullet_freeze"], SPELL_VALUE["frostbullet_range"]
        )
        self.kill()
