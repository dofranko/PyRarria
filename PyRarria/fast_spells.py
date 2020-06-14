import pygame
import random
from settings import *
from spritesheet import *
from creatures.vector import PVector
from items.item import *

vector = PVector


class SmallSpell(pygame.sprite.Sprite):
    """Super class for small spells"""

    def __init__(self, game, name, damage):
        self.groups = game.magics
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.damage = damage + PLAYER_VALUES["DAMAGE"]
        self.duration = 0
        self.stage_position = self.game.get_main_stage_position()
        if damage <= 0:  # Gdy skill ma 0 obrażeń
            self.damage = damage

    def update(self):
        """Update position of spell"""
        now = pygame.time.get_ticks()
        if now - self.start > self.duration:
            self.kill()

        main_stage_position = self.game.get_main_stage_position()
        self.rect.x = self.position.x - (self.stage_position.x - main_stage_position.x)
        self.rect.y = self.position.y - (self.stage_position.y - main_stage_position.y)
        self.update_frame(self.frame)

    def update_frame(self, cell_index):
        """Update frame of skill's animation"""
        pass


class SelfSpell(pygame.sprite.Sprite):
    """Super class for self spells"""

    def __init__(self, game, name):
        self.groups = game.magics
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name

    def activate_spell(self, bonus_value):
        """Activate bonuses of skill"""
        pass

    def deactivate_spell(self, bonus_value):
        """Deactivate bonuses if they were temporal"""
        pass


# Klasa zaklęcia smallfire, czyli podpalanie przeciwników
class SmallFire(SmallSpell):
    """Smallfire castable on enemies. Does one-time dmg"""

    def __init__(self, game, pos):
        super().__init__(game, "smallfire", 50)
        self.sheet = SpriteSheet(SPELL_SHEETS["smallfire"], 10, 6, 60)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.position = pos + vector(self.sheet.shift[4][0], self.sheet.shift[4][1] - 20)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.duration = SPELL_DURATION["smallfire"]
        self.start = pygame.time.get_ticks()
        self.frame = 0

    # Rysowanie kolejnej klatki tego efektu
    def update_frame(self, cell_index):
        """Update frame of animation"""
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index])
        self.frame += 1

    # Sprawdzanie czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        """Update spell's animation"""
        super().update()
        if self.frame == 60:
            self.frame = 0


# Klasa zaklęcia smallthunder, czyli uderzenie piorunem w przeciwnika
class SmallThunder(SmallSpell):
    """Thunder spell castable on enemies. Does one-time dmg"""

    def __init__(self, game, pos):
        super().__init__(game, "smallthunder", 50)
        self.sheet = SpriteSheet(SPELL_SHEETS["smallthunder"], 6, 4, 24)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.position = pos + vector(self.sheet.shift[4][0], self.sheet.shift[4][1] - 70)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.duration = SPELL_DURATION["smallthunder"]
        self.start = pygame.time.get_ticks()
        self.frame = 0

    # Rysowanie kolejnej klatki tego efektu
    def update_frame(self, cell_index):
        """Update frame of animation"""
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index // 3])
        self.frame += 1

    # Sprawdzanie czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        """Update spell's animation"""
        super().update()
        if self.frame == 72:
            self.frame = 0


# Klasa zaklęcia boulder, czyli głaz spada na przeciwnika
class Boulder(SmallSpell):
    """Boulder spell castable on enemies. Does one-time dmg"""

    def __init__(self, game, pos):
        super().__init__(game, "boulder", 150)
        self.sheet = SpriteSheet(SPELL_SHEETS["boulder"], 8, 8, 64)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.position = pos + vector(self.sheet.shift[4][0], self.sheet.shift[4][1] - 100)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed_y = 0.4
        self.duration = SPELL_DURATION["boulder"]
        self.start = pygame.time.get_ticks()
        self.frame = 0

    # Rysowanie kolejnej klatki tego efektu oraz zmiana prędkości opadania
    def update_frame(self, cell_index):
        """Update frame of animation"""
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 10), self.sheet.cells[cell_index // 3])
        self.frame += 1
        self.speed_y += 0.02

    # Sprawdzanie czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        """Update spell's animation"""
        super().update()
        self.position.y += self.speed_y
        if self.frame == 192:
            self.frame = 0


# Klasa zaklęcia freeze, czyli spowolnienie przeciwnika przez zamrożenie
class Freeze(SmallSpell):
    """Freeze spell castable on enemies. Freezes all enemies within range of skill for duration"""

    def __init__(self, game, pos):
        super().__init__(game, "freeze", 1)
        self.sheet = SpriteSheet(SPELL_SHEETS["freeze"], 10, 10, 86)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.position = pos + vector(self.sheet.shift[4][0], self.sheet.shift[4][1])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.duration = SPELL_DURATION["freeze"]
        self.start = pygame.time.get_ticks()
        self.frame = 0

        self.game.creatures_engine.freeze(
            Item.get_mouse_position_on_map(self.game.player, self.position), self.duration, SPELL_VALUE["freeze_range"]
        )

    # Rysowanie kolejnej klatki tego efektu
    def update_frame(self, cell_index):
        """Update frame of animation"""
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index])
        self.frame += 1

    # Sprawdzanie, czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        """Update spell's animation"""
        super().update()
        if self.frame == 86:
            self.frame = 0


# Klasa zaklęcia magicshield, czyli magiczna, ochronna tarcza dla gracza
class MagicShield(SelfSpell):
    """Shield spell. Instant cast. Gives defence bonus."""

    def __init__(self, game):
        super().__init__(game, "magicshield")
        self.sheet = SpriteSheet(SPELL_SHEETS["magicshield"], 4, 1, 4)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.game.player.rect.center
        self.defense = SPELL_VALUE["magicshield"]
        self.duration = SPELL_DURATION["magicshield"]
        self.start = pygame.time.get_ticks()
        self.frame = 0
        self.activate_spell(self.defense)

    def activate_spell(self, bonus_value):
        """Add defence bonus to player"""
        PLAYER_VALUES["DEFENCE"] += bonus_value

    def deactivate_spell(self, bonus_value):
        """Sub defence bonus from player"""
        PLAYER_VALUES["DEFENCE"] -= bonus_value

    # Rysowanie kolejnej klatki tego efektu
    def update_frame(self, cell_index):
        """Update frame of animation"""
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index // 10])
        self.frame += 1

    # Sprawdzanie czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.start > self.duration:
            self.deactivate_spell(self.defense)
            self.kill()

        self.rect.center = self.game.player.rect.center
        self.rect.y -= 5

        if self.frame == 40:
            self.frame = 0

        self.update_frame(self.frame)


# Klasa zaklęcia selfheal, czyli magiczne odnowienie zdrowia gracza
class SelfHeal(SelfSpell):
    """One-time heal player"""

    def __init__(self, game):
        super().__init__(game, "selfheal")
        self.sheet = SpriteSheet(SPELL_SHEETS["selfheal"], 4, 2, 8)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.game.player.rect.center
        self.frame = 0
        self.activate_spell(SPELL_VALUE["selfheal"])  # Magiczne dodanie punktów zdrowia

    def activate_spell(self, bonus_value):
        self.game.player.health_bar.increase_health(bonus_value)

    # Rysowanie kolejnej klatki tego efektu
    def update_frame(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index // 10])
        self.frame += 1

    def update(self):
        self.rect.center = self.game.player.rect.center
        self.rect.y -= 5

        if self.frame == 75:
            self.kill()

        self.update_frame(self.frame)


# Klasa zaklęcia bard, czyli magiczne dzwięki instrumentów
class Bard(SelfSpell):
    """Push away creatures"""

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
        self.game.creatures_engine.bard(SPELL_VALUE["bard"])

    def activate_spell(self, bonus_value):
        """Push away creatures"""
        self.game.creatures_engine.bard(bonus_value)

    # Rysowanie kolejnej klatki tego efektu
    def update_frame(self, cell_index):
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
            self.update_frame(self.frame)
        else:
            self.frame += 1
