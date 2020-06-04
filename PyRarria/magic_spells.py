import pygame
import random
from settings import *
from spritesheet import *


class Spell(pygame.sprite.Sprite):
    def __init__(self, game, name):
        self.groups = game.all_sprites, game.magics
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name


# Klasa zaklęcia fireball, czyli lecący ognisty pocisk
class Fireball(Spell):
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
        vector = pygame.math.Vector2(
            (self.game.background.start_scrolling_position.x + self.game.background.main_stage.position.x),
            (self.game.background.start_scrolling_position.y + self.game.background.main_stage.position.y),
        )
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

    def check_collision(self):
        # Detekcja kolizji ze środowiskiem
        hits_1 = pygame.sprite.spritecollide(self, self.game.platforms, False)
        for _ in hits_1:
            self.explode()

        # TODO: Detekcja kolizji z przeciwnikami
        pass

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


# Klasa zaklęcia smallfire, czyli podpalanie przeciwników
class SmallFire(Spell):
    def __init__(self, game, pos):
        super().__init__(game, "smallfire")
        self.sheet = SpriteSheet(SPELL_SHEETS["smallfire"], 10, 6, 60)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.pos = pos + (self.sheet.shift[4][0], self.sheet.shift[4][1] - 20)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        # Tutaj są właściwości, które należy później dostosować
        self.damage = 50
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
        self.rect.x = self.pos.x - (self.stage_pos_x - main_stage_position.x)
        self.rect.y = self.pos.y - (self.stage_pos_y - main_stage_position.y)

        if self.frame == 60:
            self.frame = 0

        self.draw(self.frame)


# Klasa zaklęcia frostbullet, czyli lecący lodowy pocisk
class FrostBullet(Spell):
    def __init__(self, game, pos, speed_y, direction):
        super().__init__(game, "frostbullet")
        if direction == 1:
            self.sheet = SpriteSheet(SPELL_SHEETS["frostbullet_right"], 8, 1, 8)
        else:
            self.sheet = SpriteSheet(SPELL_SHEETS["frostbullet_left"], 8, 1, 8)

        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.pos = pos
        self.rect = self.image.get_rect()
        vector = pygame.math.Vector2(
            (self.game.background.start_scrolling_position.x + self.game.background.main_stage.position.x),
            (self.game.background.start_scrolling_position.y + self.game.background.main_stage.position.y),
        )
        self.pos += vector
        self.pos.y += 5
        self.rect.center = self.pos
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

    def check_collision(self):
        # Detekcja kolizji ze środowiskiem
        hits_1 = pygame.sprite.spritecollide(self, self.game.platforms, False)
        for _ in hits_1:
            print("FRB KOL")
            self.kill()

        # TODO: Detekcja kolizji z przeciwnikami
        pass


# Klasa zaklęcia smallthunder, czyli uderzenie piorunem w przeciwnika
class SmallThunder(Spell):
    def __init__(self, game, pos):
        super().__init__(game, "smallthunder")
        self.sheet = SpriteSheet(SPELL_SHEETS["smallthunder"], 6, 4, 24)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.pos = pos + (self.sheet.shift[4][0], self.sheet.shift[4][1] - 70)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        # Tutaj są właściwości, które należy później dostosować
        self.damage = 50
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
        self.rect.x = self.pos.x - (self.stage_pos_x - main_stage_position.x)
        self.rect.y = self.pos.y - (self.stage_pos_y - main_stage_position.y)

        if self.frame == 72:
            self.frame = 0

        self.draw(self.frame)


# Klasa zaklęcia boulder, czyli głaz spada na przeciwnika
class Boulder(Spell):
    def __init__(self, game, pos):
        super().__init__(game, "boulder")
        self.sheet = SpriteSheet(SPELL_SHEETS["boulder"], 8, 8, 64)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.pos = pos + (self.sheet.shift[4][0], self.sheet.shift[4][1] - 100)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed_y = 0.4
        self.damage = 150
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
        self.rect.x = self.pos.x - (self.stage_pos_x - main_stage_position.x)
        self.rect.y = self.pos.y - (self.stage_pos_y - main_stage_position.y)
        self.pos.y += self.speed_y

        if self.frame == 192:
            self.frame = 0

        self.draw(self.frame)


# Klasa zaklęcia magicshield, czyli magiczna, ochronna tarcza dla gracza
class MagicShield(Spell):
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
        pass

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
class SelfHeal(Spell):
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
class Bard(Spell):
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
class Freeze(Spell):
    def __init__(self, game, pos):
        super().__init__(game, "freeze")
        self.sheet = SpriteSheet(SPELL_SHEETS["freeze"], 10, 10, 86)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.pos = pos + (self.sheet.shift[4][0], self.sheet.shift[4][1])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.duration = 15000
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

    # Sprawdzanie, czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.start > self.duration:
            self.kill()

        main_stage_position = self.game.get_main_stage_position()
        self.rect.x = self.pos.x - (self.stage_pos_x - main_stage_position.x)
        self.rect.y = self.pos.y - (self.stage_pos_y - main_stage_position.y)

        if self.frame == 86:
            self.frame = 0

        self.draw(self.frame)
