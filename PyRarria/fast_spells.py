import pygame
import random
from settings import *
from spritesheet import *
from creatures.vector import PVector

vector = PVector


class SmallSpell(pygame.sprite.Sprite):
    """Super class for small spells"""

    def __init__(self, game, name, damage):
        self.groups = game.all_sprites, game.magics
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        if damage > 0:
            self.damage = damage + PLAYER_VALUES["DAMAGE"]
        else:
            self.damage = damage


class SelfSpell(pygame.sprite.Sprite):
    """Super class for self spells"""

    def __init__(self, game, name):
        self.groups = game.all_sprites, game.magics
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name


# Klasa zaklęcia smallfire, czyli podpalanie przeciwników
class SmallFire(SmallSpell):
    def __init__(self, game, pos):
        super().__init__(game, "smallfire", 50)
        self.sheet = SpriteSheet(SPELL_SHEETS["smallfire"], 10, 6, 60)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.position = pos + vector(self.sheet.shift[4][0], self.sheet.shift[4][1] - 20)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.duration = 4000
        self.start = pygame.time.get_ticks()
        self.frame = 0
        main_stage_position = self.game.get_main_stage_position()
        self.stage_pos_x = main_stage_position.x
        self.stage_pos_y = main_stage_position.y

    # Rysowanie kolejnej klatki tego efektu
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index])
        self.frame += 1

    # Sprawdzanie czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.start > self.duration:
            self.kill()

        main_stage_position = self.game.get_main_stage_position()
        self.rect.x = self.position.x - (self.stage_pos_x - main_stage_position.x)
        self.rect.y = self.position.y - (self.stage_pos_y - main_stage_position.y)

        if self.frame == 60:
            self.frame = 0

        self.draw(self.frame)


# Klasa zaklęcia smallthunder, czyli uderzenie piorunem w przeciwnika
class SmallThunder(SmallSpell):
    def __init__(self, game, pos):
        super().__init__(game, "smallthunder", 50)
        self.sheet = SpriteSheet(SPELL_SHEETS["smallthunder"], 6, 4, 24)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.position = pos + vector(self.sheet.shift[4][0], self.sheet.shift[4][1] - 70)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.duration = 720
        self.start = pygame.time.get_ticks()
        self.frame = 0
        main_stage_position = self.game.get_main_stage_position()
        self.stage_pos_x = main_stage_position.x
        self.stage_pos_y = main_stage_position.y

    # Rysowanie kolejnej klatki tego efektu
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index // 3])
        self.frame += 1

    # Sprawdzanie czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.start > self.duration:
            self.kill()

        main_stage_position = self.game.get_main_stage_position()
        self.rect.x = self.position.x - (self.stage_pos_x - main_stage_position.x)
        self.rect.y = self.position.y - (self.stage_pos_y - main_stage_position.y)

        if self.frame == 72:
            self.frame = 0

        self.draw(self.frame)


# Klasa zaklęcia boulder, czyli głaz spada na przeciwnika
class Boulder(SmallSpell):
    def __init__(self, game, pos):
        super().__init__(game, "boulder", 150)
        self.sheet = SpriteSheet(SPELL_SHEETS["boulder"], 8, 8, 64)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.position = pos + vector(self.sheet.shift[4][0], self.sheet.shift[4][1] - 100)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed_y = 0.4
        self.duration = 1500
        self.start = pygame.time.get_ticks()
        self.frame = 0
        main_stage_position = self.game.get_main_stage_position()
        self.stage_pos_x = main_stage_position.x
        self.stage_pos_y = main_stage_position.y

    # Rysowanie kolejnej klatki tego efektu oraz zmiana prędkości opadania
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 10), self.sheet.cells[cell_index // 3])
        self.frame += 1
        self.speed_y += 0.02

    # Sprawdzanie czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.start > self.duration:
            self.kill()

        main_stage_position = self.game.get_main_stage_position()
        self.rect.x = self.position.x - (self.stage_pos_x - main_stage_position.x)
        self.rect.y = self.position.y - (self.stage_pos_y - main_stage_position.y)
        self.position.y += self.speed_y

        if self.frame == 192:
            self.frame = 0

        self.draw(self.frame)


# Klasa zaklęcia magicshield, czyli magiczna, ochronna tarcza dla gracza
class MagicShield(SelfSpell):
    def __init__(self, game):
        super().__init__(game, "magicshield")
        self.sheet = SpriteSheet(SPELL_SHEETS["magicshield"], 4, 1, 4)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.game.player.rect.center
        self.defense = 10
        self.duration = 60000
        self.start = pygame.time.get_ticks()
        self.frame = 0
        self.change_player_defense(self.defense)

    # Zmiana defense gracza o pewną wartość
    def change_player_defense(self, value):
        PLAYER_VALUES["DEFENCE"] += value

    # Rysowanie kolejnej klatki tego efektu
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index // 10])
        self.frame += 1

    # Sprawdzanie czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.start > self.duration:
            self.change_player_defense(-self.defense)
            self.kill()

        self.rect.center = self.game.player.rect.center
        self.rect.y -= 5

        if self.frame == 40:
            self.frame = 0

        self.draw(self.frame)


# Klasa zaklęcia selfheal, czyli magiczne odnowienie zdrowia gracza
class SelfHeal(SelfSpell):
    def __init__(self, game):
        super().__init__(game, "selfheal")
        self.sheet = SpriteSheet(SPELL_SHEETS["selfheal"], 4, 2, 8)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.game.player.rect.center
        self.frame = 0
        self.game.health_bar.increase_health(200)  # Magiczne dodanie punktów zdrowia

    # Rysowanie kolejnej klatki tego efektu
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index // 10])
        self.frame += 1

    def update(self):
        self.rect.center = self.game.player.rect.center
        self.rect.y -= 5

        if self.frame == 75:
            self.kill()

        self.draw(self.frame)


# Klasa zaklęcia bard, czyli magiczne dzwięki instrumentów
class Bard(SelfSpell):
    def __init__(self, game):
        super().__init__(game, "bard")
        index = random.randint(0, 3)
        if index == 0:
            self.sheet = SpriteSheet(SPELL_SHEETS["bard_1"], 5, 1, 5)
        elif index == 1:
            self.sheet = SpriteSheet(SPELL_SHEETS["bard_2"], 5, 1, 5)
        else:
            self.sheet = SpriteSheet(SPELL_SHEETS["bard_3"], 5, 1, 5)

        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.game.player.rect.center
        self.offset_x = random.uniform(-40, 40)
        self.frame = 0
        self.game.creatures_engine.bard(1.0)

    # Rysowanie kolejnej klatki tego efektu
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index // 6])
        self.frame += 1

    # Sprawdzanie czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        self.rect.center = self.game.player.rect.center
        self.rect.centery -= 60
        self.rect.centerx -= self.offset_x

        if self.frame == 36:
            self.kill()
        if self.frame in [6 * i for i in range(0, 5)]:
            self.draw(self.frame)
        else:
            self.frame += 1


# Klasa zaklęcia freeze, czyli spowolnienie przeciwnika przez zamrożenie
class Freeze(SmallSpell):
    def __init__(self, game, pos):
        super().__init__(game, "freeze", 1)
        self.sheet = SpriteSheet(SPELL_SHEETS["freeze"], 10, 10, 86)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.position = pos + vector(self.sheet.shift[4][0], self.sheet.shift[4][1])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.duration = 15000
        self.start = pygame.time.get_ticks()
        self.frame = 0
        main_stage_position = self.game.get_main_stage_position()
        self.stage_pos_x = main_stage_position.x
        self.stage_pos_y = main_stage_position.y
        self.freezed_enemies = [
            [enemy, enemy.maxspeed] for enemy in self.game.all_creatures if pygame.sprite.collide_rect(enemy, self)
        ]
        # self.freeze_enemies()
        self.game.creatures_engine.freeze(100)

    def freeze_enemies(self):
        for enemy, _ in self.freezed_enemies:
            enemy.maxspeed = 0

    def defreeze_enemies(self):
        for enemy, maxspeed in self.freezed_enemies:
            enemy.maxspeed = maxspeed

    # Rysowanie kolejnej klatki tego efektu
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index])
        self.frame += 1

    # Sprawdzanie, czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.start > self.duration:
            self.defreeze_enemies()
            self.kill()

        main_stage_position = self.game.get_main_stage_position()
        self.rect.x = self.position.x - (self.stage_pos_x - main_stage_position.x)
        self.rect.y = self.position.y - (self.stage_pos_y - main_stage_position.y)

        if self.frame == 86:
            self.frame = 0

        self.draw(self.frame)
