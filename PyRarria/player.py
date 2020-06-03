# Sprite class for player
import pygame
from settings import *
from magic_spells import *
import random

from PyRarria.creatures.vector import PVector

vector = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    # Standardowo:   ^ position.x, position.y - pozycja względem całej mapy gry
    #               ^ rect.x, rect.y - pozycja względem monitora
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((30, 40), pygame.SRCALPHA)
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.position = vector(WIDTH / 2, 0)
        self.vel = vector(0, 0)
        self.acc = vector(0, PLAYER_GRAV)
        self.mask = pygame.mask.from_surface(self.image)
        self.facing = 1
        self.standing = False
        self.q_trigger = False
        self.trzymany = None
        self.last_shift = 0
        self.spell_cast_ready = False

        # TODO usunac location i damage
        self.location = PVector(self.position.x, self.position.y)
        self.damage = 10

        # info kiedy gracz ostatnio użył danego zaklęcia
        self.last_cast = {
            'fireball': -SPELL_DELAYS['fireball'],
            'smallfire': -SPELL_DELAYS['smallfire'],
            'frostbullet': -SPELL_DELAYS['frostbullet'],
            'smallthunder': -SPELL_DELAYS['smallthunder'],
            'boulder': -SPELL_DELAYS['boulder'],
            'magicshield': -SPELL_DELAYS['magicshield'],
            'selfheal': -SPELL_DELAYS['selfheal'],
            'bard': -SPELL_DELAYS['bard'],
            'freeze': -SPELL_DELAYS['freeze']
        }

        # Tutaj na tę chwilę zaklęcia przypisane do tych trzech klawiszy (+ klik myszki dla shift)
        self.spell_ctrl = None
        self.spell_shift = 'smallthunder'
        self.spell_key = None

    def jump(self):
        # Skok tylko, jeśli stoi się na platformie
        self.vel.y = -20

    # Sprawdzenie kolizji (stania) od góry platform
    def check_collision_vertically(self):
        can_jump = False
        # Gdy porusza się w dół
        if self.vel.y > 0:
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)  # False -> don't remove from platforms
            if hits:
                new_position = min([hits[i].position.y for i in range(len(hits))])
                new_position += -(HEIGHT // 2 + self.rect.height)  # SPECIAL ALIGN
                self.rect.y += new_position - self.position.y  # Cofnięcie na wcześniejszą pozycję (przed sprawdzaniem kolizji)
                self.position.y = new_position
                self.vel.y = 0
                can_jump = True
        # Gdy porusza się w górę
        elif -19 < self.vel.y < 0:
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)  # False -> don't remove from platforms
            if hits:
                new_position = max([hits[i].position.y + hits[i].rect.height + 1 for i in range(len(hits))])
                new_position += -(HEIGHT // 2)  # SPECIAL ALIGN
                self.rect.y += new_position - self.position.y  # Cofnięcie na wcześniejszą pozycję (przed sprawdzaniem kolizji)
                self.position.y = new_position
                self.vel.y = 0
        return can_jump

    def check_collision_horizontally(self):
        # Gdy porusza się w prawo
        if self.acc.x > 0:
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)  # False -> don't remove from platforms
            if hits:
                self.position.x = min([hits[i].position.x for i in range(len(hits))])
                self.position.x += -(WIDTH // 2) - self.rect.width  # SPECIAL ALIGN
                self.acc.x = 0
        # Gdy porusza się w lewo
        elif self.acc.x < 0:
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)  # False -> don't remove from platforms
            if hits:
                self.position.x = max([hits[i].position.x + hits[i].rect.width for i in range(len(hits))])
                self.position.x += -WIDTH // 2  # SPECIAL ALIGN
                self.acc.x = 0

    # Sprawdzanie kolizji boosterów (prostokątów gracza i ich)
    def check_collision_boosters(self):
        hits = pygame.sprite.spritecollide(self, self.game.boosters, False)  # , pygame.sprite.collide_mask)
        for hit in hits:
            kill = False
            if hit.name == 'health':
                if self.game.health_bar.add_heart():
                    kill = True
            elif hit.name == 'mana':
                if self.game.mana_bar.add_star():
                    kill = True
            elif hit.name in ['boost_damage', 'boost_defense', 'boost_player_speed', 'boost_accuracy']:
                # Sprawdzanie prawdziwej kolizji (mask collision)
                clip = self.rect.clip(hit.rect)
                collision = hit.check_true_collision(clip, self.rect, self.mask)
                if collision:
                    hit.apply_boost()
            if kill:
                hit.kill()

    def handle_mouse_cast_spell(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.spell_cast_ready:
                # Tutaj docelowo ma iterować po potworach
                for sprite in self.game.all_sprites:
                    if sprite.rect.collidepoint(event.pos):
                        if self.game.mana_bar.mana - SPELL_COST[self.spell_key] >= 0:
                            self.last_cast[self.spell_key] = pygame.time.get_ticks()
                            cur_pos = vector(event.pos[0], event.pos[1])
                            if self.spell_key == 'smallthunder':
                                SmallThunder(self.game, cur_pos)
                            elif self.spell_key == 'smallfire':
                                SmallFire(self.game, cur_pos)
                            elif self.spell_key == "boulder":
                                Boulder(self.game, cur_pos)
                            else:
                                Freeze(self.game, cur_pos)
                            self.game.mana_bar.decrease_mana(SPELL_COST[self.spell_shift])
                            self.game.spells.chosen = None
                            self.spell_cast_ready = False

    # zbiera itemy
    def collect(self):
        collected = pygame.sprite.spritecollide(self, self.game.items, True)
        for it in collected:
            self.game.all_sprites.remove(it)
            if not self.game.equipment.add_item(it):
                print("pelne eq")

    # wyrzuca aktywny przedmiot
    def throw(self):
        wyrzucony = self.game.equipment.remove_item("active")
        if not wyrzucony:
            return

        wyrzucony.pos_x = self.position.x + 80 * self.facing + 15 + WIDTH / 2
        wyrzucony.pos_y = self.position.y - 50 + HEIGHT / 2
        self.game.all_sprites.add(wyrzucony)
        self.game.items.add(wyrzucony)

    def update(self):

        self.location.set(self.rect.centerx, self.rect.centery)

        # Równania ruchu. Zabawa na własną odpowiedzialność :v
        self.vel.y += self.acc.y
        if self.vel.y > MAX_VEL_Y:
            self.vel.y = MAX_VEL_Y

        # Poruszenie się i sprawdzenie kolizji
        self.position.y += self.vel.y + 0.5 * self.acc.y
        self.rect.y += self.vel.y + 0.5 * self.acc.y
        can_jump = self.check_collision_vertically()

        self.position.x += self.acc.x
        self.rect.x += self.acc.x
        self.check_collision_horizontally()

        self.collect()
        self.trzymany = self.game.equipment.get_active_item()
        self.game.trzymany = self.trzymany

        # Sprawdzanie kolizji z boosterami
        self.check_collision_boosters()

        # To zostaje nadpisane, jeśli działa tło (background.py) w klasie tła @see class Background
        self.rect.midbottom = (self.position.x, self.position.y)

        # Zmiana wektorów przyspieszenia gracza, gdy wciśnięte przyciski poruszania
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.facing = -1
            self.acc.x = -PLAYER_MOVE['PLAYER_ACC']
            self.standing = False
        elif keys[pygame.K_RIGHT]:
            self.facing = 1
            self.acc.x = PLAYER_MOVE['PLAYER_ACC']
            self.standing = False
        else:
            self.acc.x = 0
            self.standing = True
        if keys[pygame.K_UP] and can_jump:
            self.standing = False
            self.jump()

        if keys[pygame.K_q]:
            if not self.q_trigger:
                self.throw()
            self.q_trigger = True
        else:
            self.q_trigger = False


        # Wystrzeliwanie magicznych pocisków, gdy wciśnięty ctrl
        if keys[pygame.K_LCTRL]:
            if self.spell_ctrl is not None:
                now_ctrl = pygame.time.get_ticks()
                if now_ctrl - self.last_cast[self.spell_ctrl] > SPELL_DELAYS[self.spell_ctrl]:
                    if self.game.mana_bar.mana - SPELL_COST[self.spell_ctrl] >= 0:
                        self.last_cast[self.spell_ctrl] = now_ctrl
                        self.game.spells.flag_ctrl = True
                        self.game.spells.last_ctrl = now_ctrl
                        if self.facing == 1:
                            cur_pos = vector(self.position.x + 10, self.rect.centery + 10)
                        else:
                            cur_pos = vector(self.position.x - 25, self.rect.centery + 10)
                        # Prędkość pionowa pocisku po wystrzeleniu
                        speed_y = random.uniform(-0.2, 0.2)
                        if self.spell_ctrl == 'fireball':
                            Fireball(self.game, cur_pos, speed_y, self.facing)
                        elif self.spell_ctrl == 'frostbullet':
                            FrostBullet(self.game, cur_pos, speed_y, self.facing)
                        self.game.mana_bar.decrease_mana(SPELL_COST[self.spell_ctrl])
        # zmiana ataku podstawowego, gdy wciśnięty shift
        elif keys[pygame.K_LSHIFT]:
            now_shift = pygame.time.get_ticks()
            if now_shift - self.last_shift > 200:
                self.last_shift = now_shift
                if self.spell_ctrl is None:
                    self.spell_ctrl = 'fireball'
                    self.game.spells.special += 1
                elif self.spell_ctrl == 'fireball':
                    self.spell_ctrl = 'frostbullet'
                    self.game.spells.special += 1
                else:
                    self.spell_ctrl = None
                    self.game.spells.special = 7

        # Tutaj w zaklęcie "uzbraja się" klawiszami 7, 8, 9, 0
        # lub tymi klawiszami automatycznie się wykonuje zaklęcie
        elif keys[pygame.K_7]:
            self.spell_key = self.game.spells.get_spell_at(0)
            self.execute(0)
        elif keys[pygame.K_8]:
            self.spell_key = self.game.spells.get_spell_at(1)
            self.execute(1)
        elif keys[pygame.K_9]:
            self.spell_key = self.game.spells.get_spell_at(2)
            self.execute(2)
        elif keys[pygame.K_0]:
            self.spell_key = self.game.spells.get_spell_at(3)
            self.execute(3)

    def execute(self, number):
        now_key = pygame.time.get_ticks()
        if now_key - self.last_cast[self.spell_key] > SPELL_DELAYS[self.spell_key]:
            if self.game.mana_bar.mana - SPELL_COST[self.spell_key] >= 0:
                self.game.spells.chosen = number
                if self.spell_key in ["selfheal", "magicshield", "bard"]:
                    self.last_cast[self.spell_key] = now_key
                    self.game.spells.flag_key = True
                    self.game.spells.last_key = now_key
                    if self.spell_key == 'selfheal':
                        SelfHeal(self.game)
                    elif self.spell_key == 'magicshield':
                        MagicShield(self.game)
                    else:
                        Bard(self.game)
                    self.game.mana_bar.decrease_mana(SPELL_COST[self.spell_key])
                else:
                    self.spell_cast_ready = True

    def hit(self, attack):
        print(f'attack: {attack}')
