import pygame
import pytweening
from settings import *
from spritesheet import *

vector = pygame.math.Vector2


class Booster(pygame.sprite.Sprite):
    def __init__(self, game, pos, name, lifespan):
        self.groups = game.boosters
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.position = pos
        self.lifespan = lifespan
        self.start_displaying = pygame.time.get_ticks()

    # Sprawdzanie, czy możliwy czas zebrania boostera minął
    def check_lifespan(self):
        now = pygame.time.get_ticks()
        if now - self.start_displaying > self.lifespan:
            self.kill()


# Klasa boosterów oscylujących (zalicza się booster health i mana)
class TweeningBooster(Booster):
    def __init__(self, game, pos, name):
        super().__init__(game, pos, name, 70000)
        self.image = pygame.image.load(BOOSTERS_SHEETS[name]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.tween = pytweening.easeInOutSine
        self.step = 0
        self.dir = 1

    # Aktualizacja pozycji w oscylacji
    def update(self):
        self.check_lifespan()
        main_stage_position = self.game.get_main_stage_position()
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.x = self.position.x + main_stage_position.x
        self.rect.y = self.position.y + main_stage_position.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1

    def apply_boost(self):
        if self.name == "health":
            self.game.player.health_bar.add_heart()
        elif self.name == "mana":
            self.game.player.mana_bar.add_star()
        self.kill()


# Klasa boosterów z animacją (damage, defense, player speed, accuracy)
class SpinningBooster(Booster):
    def __init__(self, game, pos, name, lifespan):
        super().__init__(game, pos, name, lifespan)
        self.sheet = SpriteSheet(BOOSTERS_SHEETS[name], ANIM[self.name][0], ANIM[self.name][1], ANIM[self.name][2])
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.frame = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.active = False
        self.start_boost = 0

    # Rysowanie kolejnej klatki tego efektu/aktualizacja maski
    def update_frame(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index])
        self.mask = pygame.mask.from_surface(self.image)
        self.frame += 1

    def apply_boost(self):
        if self.start_boost != 0:
            return False
        self.active = True
        self.game.boosters.remove(self)
        self.game.active_boosters.add(self)
        self.image.fill((0, 0, 0, 0))
        self.start_boost = pygame.time.get_ticks()
        return True

    def update(self):
        if self.active:
            now = pygame.time.get_ticks()
            if now - self.start_boost > self.duration:
                self.disapply_boost()
                self.kill()
        else:
            main_stage_position = self.game.get_main_stage_position()
            self.rect.x = self.position.x + main_stage_position.x
            self.rect.y = self.position.y + main_stage_position.y

            if self.frame == ANIM[self.name][2]:
                self.frame = 0
            self.update_frame(self.frame)


# Booster czasowo zwiększający damage gracza
class DamageBooster(SpinningBooster):
    def __init__(self, game, pos):
        super().__init__(game, pos, "damage_booster", 70000)
        self.duration = BOOSTERS_DURATIONS["damage_booster"]  # Czas trwania efektu po podniesieniu

    # Aktywacja boostera / Zmiana wartości zadawanych obrażeń
    def apply_boost(self, value=BOOSTERS_VALUE["damage"]):
        if super().apply_boost():
            PLAYER_VALUES["DAMAGE"] += value

    def disapply_boost(self, value=BOOSTERS_VALUE["damage"]):
        PLAYER_VALUES["DAMAGE"] -= value


# Booster czasowo zwiększający defense gracza
class DefenseBooster(SpinningBooster):
    def __init__(self, game, pos):
        super().__init__(game, pos, "defense_booster", 70000)
        self.duration = BOOSTERS_DURATIONS["defense_booster"]  # Czas trwania efektu po podniesieniu

    # Aktywacja boostera / Zmiana wartości defense gracza
    def apply_boost(self, value=BOOSTERS_VALUE["defense"]):
        if super().apply_boost():
            PLAYER_VALUES["DEFENCE"] += value

    def disapply_boost(self, value=BOOSTERS_VALUE["defense"]):
        PLAYER_VALUES["DEFENCE"] -= value


# Booster czasowo zwiększający prędkość poruszania się gracza
class SpeedBooster(SpinningBooster):
    def __init__(self, game, pos):
        super().__init__(game, pos, "speed_booster", 70000)
        self.duration = 10000  # Czas trwania efektu po podniesieniu

    # Aktywacja boostera / Zmiana wartości prędkości gracza
    def apply_boost(self, value=BOOSTERS_VALUE["speed"]):
        if super().apply_boost():
            PLAYER_MOVE["PLAYER_ACC"] += value

    def disapply_boost(self, value=BOOSTERS_VALUE["speed"]):
        PLAYER_MOVE["PLAYER_ACC"] -= value


# Booster czasowo zwiększający celność gracza
class AccuracyBooster(SpinningBooster):
    def __init__(self, game, pos):
        super().__init__(game, pos, "accuracy_booster", 70000)
        self.duration = BOOSTERS_DURATIONS["accuracy_booster"]  # Czas trwania efektu po podniesieniu

    # Aktywacja boostera / Zmiana wartości celności gracza
    def apply_boost(self, value=BOOSTERS_VALUE["accuracy"]):
        if super().apply_boost():
            PLAYER_VALUES["ACCURACY"] += value

    def disapply_boost(self, value=BOOSTERS_VALUE["accuracy"]):
        PLAYER_VALUES["ACCURACY"] -= value
