import pygame
import random
from settings import *
from spritesheet import *


class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, pos, vect):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.sheet = SpriteSheet(SPELL_SHEETS["collision_explosion"], 10, 6, 60)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.pos = pos + (self.sheet.shift[4][0], self.sheet.shift[4][1])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.start = pygame.time.get_ticks()
        self.frame = 0
        self.stage_pos_x = vect.x
        self.stage_pos_y = vect.y

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
        self.rect.x = self.pos.x - (self.stage_pos_x - main_stage_position.x)
        self.rect.y = self.pos.y - (self.stage_pos_y - main_stage_position.y)


class BulletSpell(pygame.sprite.Sprite):
    """Super class for spells"""

    def __init__(self, game, name, damage=0):
        self.groups = game.all_sprites, game.magics
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.damage = damage

    def check_collision(self):
        # Detekcja kolizji z przeciwnikami
        hits = pygame.sprite.spritecollide(self, self.game.all_creatures, False)
        if hits:
            self.explode()
            hits[0].hit(self.damage + PLAYER_VALUES["DAMAGE"])

        # Detekcja kolizji ze środowiskiem
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            self.explode()

    def explode(self):
        """Make explosion after colliding with object (should override)"""
        self.kill()


# Klasa zaklęcia fireball, czyli lecący ognisty pocisk
class Fireball(BulletSpell):
    def __init__(self, game, pos, speed_y, direction):
        super().__init__(game, "fireball")
        if direction == 1:
            self.sheet = SpriteSheet(SPELL_SHEETS["fireball_right"], 8, 8, 64)
        else:
            self.sheet = SpriteSheet(SPELL_SHEETS["fireball_left"], 8, 8, 64)

        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.frame = random.randint(0, 63)
        self.pos = pos
        self.rect = self.image.get_rect()
        vector = self.game.get_main_stage_position()
        pos += vector
        self.rect.center = pos
        # Tutaj są właściwości, które należy później dostosować
        self.damage = 50
        self.speed_x = 3
        self.speed_y = speed_y
        self.accuracy = 0.95
        self.direction = direction
        self.duration = 4000
        self.start = pygame.time.get_ticks()
        main_stage_position = self.game.get_main_stage_position()
        self.stage_pos_x = main_stage_position.x
        self.stage_pos_y = main_stage_position.y

    # Rysowanie kolejnej klatki tego efektu
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[int(cell_index)])
        self.frame += 1

    # Sprawdzanie czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.start > self.duration:
            self.kill()

        main_stage_position = self.game.get_main_stage_position()
        self.rect.x = self.pos.x - (self.stage_pos_x - main_stage_position.x)
        self.rect.y = self.pos.y - (self.stage_pos_y - main_stage_position.y)
        self.pos.x += self.speed_x * self.direction
        self.rect.x += self.speed_x * self.direction
        self.pos.y += self.speed_y
        self.rect.y += self.speed_y

        if self.frame == 64:
            self.frame = 0

        self.draw(self.frame)
        self.check_collision()

    def explode(self):
        vect = pygame.math.Vector2(self.stage_pos_x, self.stage_pos_y)
        if self.direction == 1:
            vector = pygame.math.Vector2(self.pos[0] + 50, self.pos[1] + 10)
            new_explosion = Explosion(self.game, vector, vect)
        else:
            vector = pygame.math.Vector2(self.pos[0], self.pos[1] + 10)
            new_explosion = Explosion(self.game, vector, vect)

        self.game.explosions.add(new_explosion)
        self.game.all_sprites.add(new_explosion)
        self.kill()


# Klasa zaklęcia frostbullet, czyli lecący lodowy pocisk
class FrostBullet(BulletSpell):
    def __init__(self, game, pos, speed_y, direction):
        super().__init__(game, "frostbullet")
        if direction == 1:
            self.sheet = SpriteSheet(SPELL_SHEETS["frostbullet_right"], 8, 1, 8)
        else:
            self.sheet = SpriteSheet(SPELL_SHEETS["frostbullet_left"], 8, 1, 8)

        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.pos = pos
        self.rect = self.image.get_rect()
        vector = self.game.get_main_stage_position()
        pos += vector
        self.rect.center = pos
        # Tutaj są właściwości, które należy później dostosować
        self.damage = 50
        self.speed_x = 3
        self.speed_y = speed_y
        self.accuracy = 0.95
        self.direction = direction
        self.duration = 3000
        self.start = pygame.time.get_ticks()
        self.frame = 0
        main_stage_position = self.game.get_main_stage_position()
        self.stage_pos_x = main_stage_position.x
        self.stage_pos_y = main_stage_position.y

    # Rysowanie kolejnej klatki tego efektu
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[int(cell_index)])
        self.frame += 1

    # Sprawdzanie, czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.start > self.duration:
            self.kill()

        main_stage_position = self.game.get_main_stage_position()
        self.rect.x = self.pos.x - (self.stage_pos_x - main_stage_position.x)
        self.rect.y = self.pos.y - (self.stage_pos_y - main_stage_position.y)
        self.pos.x += self.speed_x * self.direction
        self.rect.x += self.speed_x * self.direction
        self.pos.y += self.speed_y
        self.rect.y += self.speed_y

        if self.frame == 8:
            self.frame = 0

        self.draw(self.frame)
        self.check_collision()
