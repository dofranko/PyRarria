import pygame
import pytweening
from settings import *
from spritesheet import *

vector = pygame.math.Vector2


class Booster(pygame.sprite.Sprite):
    def __init__(self, game, pos, name, lifespan):
        self.groups = game.all_sprites, game.boosters
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.pos = pos
        self.lifespan = lifespan
        self.start = pygame.time.get_ticks()

    # Sprawdzanie, czy możliwy czas zebrania boostera minął
    def check_lifespan(self):
        now = pygame.time.get_ticks()
        if now - self.start > self.lifespan:
            self.kill()


# Klasa boosterów oscylujących (zalicza się booster health i mana)
class TweeningBooster(Booster):
    def __init__(self, game, pos, name):
        super().__init__(game, pos, name, 70000)
        self.image = pygame.image.load(BOOSTERS_SHEETS[name]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.pos = pos
        self.rect = self.image.get_rect()
        self.tween = pytweening.easeInOutSine
        self.step = 0
        self.dir = 1

    # Aktualizacja pozycji w oscylacji
    def update(self):
        self.check_lifespan()
        main_stage_position = self.game.get_main_stage_position()
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.x = self.pos.x + main_stage_position.x
        self.rect.y = self.pos.y + main_stage_position.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1


# Klasa boosterów z animacją (damage, defense, player speed, accuracy)
class SpinningBooster(Booster):
    def __init__(self, game, pos, name, lifespan):
        super().__init__(game, pos, name, lifespan)
        self.sheet = SpriteSheet(BOOSTERS_SHEETS[name], ANIM[self.name][0], ANIM[self.name][1], ANIM[self.name][2])
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.frame = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.active = False

    # Rysowanie kolejnej klatki tego efektu/aktualizacja maski
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index])
        self.mask = pygame.mask.from_surface(self.image)
        self.frame += 1

    # Sprawdzanie prawdziwej kolizji (mask collision)
    def check_true_collision(self, clip, player_rect, player_mask):
        x1, y1 = clip.x - player_rect.x, clip.y - player_rect.y
        x2, y2 = clip.x - self.rect.x, clip.y - self.rect.y
        for x in range(clip.width):
            for y in range(clip.height):
                if player_mask.get_at((x1 + x, y1 + y)) and self.mask.get_at((x2 + x, y2 + y)):
                    return True


# Booster czasowo zwiększający damage gracza
class DamageBooster(SpinningBooster):
    def __init__(self, game, pos):
        super().__init__(game, pos, "boost_damage", 70000)
        self.duration = 10000  # Czas trwania efektu po podniesieniu
        self.start = 0
        self.active = False

    # Aktywacja boostera / Zmiana wartości zadawanych obrażeń
    def apply_boost(self, value=BOOSTERS_VALUE['damage']):
        if self.start == 0:
            self.active = True
            self.game.boosters.remove(self)
            self.game.active_boosters.add(self)
            self.image.fill((0, 0, 0, 0))
            self.start = pygame.time.get_ticks()
            # TODO Aktywowanie damage boost dla playera

    # Sprawdzanie, czy jego czas działania upłynął | aktualizacja pozycji i rysowanie (jeśli gracz nie podniósł)
    def update(self):
        if self.active:
            now = pygame.time.get_ticks()
            if now - self.start > self.duration:
                self.apply_boost(-BOOSTERS_VALUE['damage'])
                self.kill()
        else:
            self.check_lifespan()
            main_stage_position = self.game.get_main_stage_position()
            self.rect.x = self.pos.x + main_stage_position.x
            self.rect.y = self.pos.y + main_stage_position.y

            if self.frame == ANIM[self.name][2]:
                self.frame = 0

            self.draw(self.frame)


# Booster czasowo zwiększający defense gracza
class DefenseBooster(SpinningBooster):
    def __init__(self, game, pos):
        super().__init__(game, pos, "boost_defense", 70000)
        self.duration = 15000  # Czas trwania efektu po podniesieniu
        self.start = 0
        self.active = False

    # Aktywacja boostera / Zmiana wartości defense gracza
    def apply_boost(self, value=BOOSTERS_VALUE['defense']):
        if self.start == 0:
            self.active = True
            self.game.boosters.remove(self)
            self.game.active_boosters.add(self)
            self.image.fill((0, 0, 0, 0))
            self.start = pygame.time.get_ticks()
            # TODO Aktywowanie defense boost dla playera

    # Sprawdzanie, czy jego czas działania upłynął | aktualizacja pozycji i rysowanie (jeśli gracz nie podniósł)
    def update(self):
        if self.active:
            now = pygame.time.get_ticks()
            if now - self.start > self.duration:
                self.apply_boost(-BOOSTERS_VALUE['defense'])
                self.kill()
        else:
            self.check_lifespan()
            main_stage_position = self.game.get_main_stage_position()
            self.rect.x = self.pos.x + main_stage_position.x
            self.rect.y = self.pos.y + main_stage_position.y

            if self.frame == ANIM[self.name][2]:
                self.frame = 0

            self.draw(self.frame)


# Booster czasowo zwiększający prędkość poruszania się gracza
class PlayerSpeedBooster(SpinningBooster):
    def __init__(self, game, pos):
        super().__init__(game, pos, "boost_player_speed", 70000)
        self.duration = 10000  # Czas trwania efektu po podniesieniu
        self.start = 0
        self.active = False

    # Aktywacja boostera / Zmiana wartości prędkości gracza
    def apply_boost(self, value=BOOSTERS_VALUE['player_speed']):
        if self.start == 0:
            self.active = True
            self.game.boosters.remove(self)
            self.game.active_boosters.add(self)
            self.image.fill((0, 0, 0, 0))
            self.start = pygame.time.get_ticks()
        PLAYER_MOVE['PLAYER_ACC'] += value

    # Sprawdzanie, czy jego czas działania upłynął | aktualizacja pozycji i rysowanie (jeśli gracz nie podniósł)
    def update(self):
        if self.active:
            now = pygame.time.get_ticks()
            if now - self.start > self.duration:
                self.apply_boost(-BOOSTERS_VALUE['player_speed'])
                self.kill()
        else:
            self.check_lifespan()
            main_stage_position = self.game.get_main_stage_position()
            self.rect.x = self.pos.x + main_stage_position.x
            self.rect.y = self.pos.y + main_stage_position.y

            if self.frame == ANIM[self.name][2]:
                self.frame = 0

            self.draw(self.frame)


# Booster czasowo zwiększający celność gracza
class AccuracyBooster(SpinningBooster):
    def __init__(self, game, pos):
        super().__init__(game, pos, "boost_accuracy", 70000)
        self.duration = 15000  # Czas trwania efektu po podniesieniu
        self.start = 0
        self.active = False

    # Aktywacja boostera / Zmiana wartości celności gracza
    def apply_boost(self, value=BOOSTERS_VALUE['accuracy']):
        if self.start == 0:
            self.active = True
            self.game.boosters.remove(self)
            self.game.active_boosters.add(self)
            self.image.fill((0, 0, 0, 0))
            self.start = pygame.time.get_ticks()
            # TODO Aktywowanie accuracy boost dla playera

    # Sprawdzanie, czy jego czas działania upłynął | aktualizacja pozycji i rysowanie (jeśli gracz nie podniósł)
    def update(self):
        if self.active:
            now = pygame.time.get_ticks()
            if now - self.start > self.duration:
                self.apply_boost(-BOOSTERS_VALUE['accuracy'])
                self.kill()
        else:
            self.check_lifespan()
            main_stage_position = self.game.get_main_stage_position()
            self.rect.x = self.pos.x + main_stage_position.x
            self.rect.y = self.pos.y + main_stage_position.y

            if self.frame == ANIM[self.name][2]:
                self.frame = 0

            self.draw(self.frame)
