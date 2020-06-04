# Sprite class for player
import pygame
from settings import *
from magic_spells import *
import random

from creatures.vector import PVector

vector = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    """Sprite class for player"""

    # Standardowo:   ^ position.x, position.y - pozycja względem całej mapy gry
    #               ^ rect.x, rect.y - pozycja względem monitora
    def __init__(self, game, equipment, health_bar, mana_bar, spells):
        super().__init__()
        self.game = game
        self.equipment = equipment
        self.image = pygame.image.load(IMAGES_LIST["player"])
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.position = vector(WIDTH / 2, 0)
        self.vel = vector(0, 0)
        self.acc = vector(0, PLAYER_GRAV)
        self.mask = pygame.mask.from_surface(self.image)
        self.facing = 1
        self.standing = False  # TODO jakie mialo byc tego przeznaczenie?
        self.q_trigger = False
        self.held_item = None
        self.last_shift = 0
        self.spell_cast_ready = False

        self.health_bar = health_bar
        self.mana_bar = mana_bar
        self.spells = spells
        # TODO usunac location i damage
        self.location = PVector(self.position.x, self.position.y)
        self.damage = 10

        # info kiedy gracz ostatnio użył danego zaklęcia
        self.last_cast = {
            "fireball": -SPELL_DELAYS["fireball"],
            "smallfire": -SPELL_DELAYS["smallfire"],
            "frostbullet": -SPELL_DELAYS["frostbullet"],
            "smallthunder": -SPELL_DELAYS["smallthunder"],
            "boulder": -SPELL_DELAYS["boulder"],
            "magicshield": -SPELL_DELAYS["magicshield"],
            "selfheal": -SPELL_DELAYS["selfheal"],
            "bard": -SPELL_DELAYS["bard"],
            "freeze": -SPELL_DELAYS["freeze"],
        }

        # Tutaj na tę chwilę zaklęcia przypisane do tych trzech klawiszy (+ klik myszki dla shift)
        self.spell_ctrl = None
        self.spell_key = None

    def jump(self):
        """Player jumps (only if on platform) - change velocity y value"""
        self.vel.y = JUMP_VEL

    # Sprawdzenie kolizji (stania) od góry platform
    def check_collision_vertically(self):
        """Check collistion up/down and move if collided
            return if player standing on platform
        """
        can_jump = False
        # Gdy porusza się w dół
        if self.vel.y > 0:
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
            if hits:
                new_position = min([hits[i].position.y for i in range(len(hits))])
                new_position += -(HEIGHT // 2 + self.rect.height)  # SPECIAL ALIGN
                # Cofnięcie na wcześniejszą pozycję (przed sprawdzaniem kolizji)
                self.rect.y += new_position - self.position.y
                self.position.y = new_position
                self.vel.y = 0
                can_jump = True

        # Gdy porusza się w górę
        elif JUMP_VEL <= self.vel.y < 0:
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
            if hits:
                new_position = max([hits[i].position.y + hits[i].rect.height + 1 for i in range(len(hits))])
                new_position += -(HEIGHT // 2)  # SPECIAL ALIGN
                # Cofnięcie na wcześniejszą pozycję (przed sprawdzaniem kolizji)
                self.rect.y += new_position - self.position.y
                self.position.y = new_position
                self.vel.y = 0
        return can_jump

    def check_collision_horizontally(self):
        """Check collistion left/right and move if collided"""
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
        """Check if player collected boosters"""
        hits = pygame.sprite.spritecollide(self, self.game.boosters, False)  # , pygame.sprite.collide_mask)
        for hit in hits:
            kill = False
            if hit.name == "health":
                if self.health_bar.add_heart():
                    kill = True
            elif hit.name == "mana":
                if self.mana_bar.add_star():
                    kill = True
            elif hit.name in ["boost_damage", "boost_defense", "boost_player_speed", "boost_accuracy"]:
                # Sprawdzanie prawdziwej kolizji (mask collision)
                clip = self.rect.clip(hit.rect)
                collision = hit.check_true_collision(clip, self.rect, self.mask)
                if collision:
                    hit.apply_boost()
            if kill:
                hit.kill()

    def handle_mouse_cast_spell(self, event):
        """Handle mouse spell casting and cast if needed"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.spell_cast_ready:
                # Castowanie tylko na potwory
                for sprite in self.game.all_creatures:
                    if sprite.rect.collidepoint(event.pos):
                        if self.mana_bar.decrease_mana(SPELL_COST[self.spell_key]):
                            self.last_cast[self.spell_key] = pygame.time.get_ticks()
                            cur_pos = vector(event.pos[0], event.pos[1])
                            if self.spell_key == "smallthunder":
                                thrown_spell = SmallThunder(self.game, cur_pos)
                            elif self.spell_key == "smallfire":
                                thrown_spell = SmallFire(self.game, cur_pos)
                            elif self.spell_key == "boulder":
                                thrown_spell = Boulder(self.game, cur_pos)
                            elif self.spell_key == "freeze":
                                thrown_spell = Freeze(self.game, cur_pos)
                            sprite.hit(thrown_spell.damage)
                            self.spells.chosen = None
                            self.spell_cast_ready = False

    def collect(self):
        """Adding item to eq that was collided"""
        collected = pygame.sprite.spritecollide(self, self.game.items, False)
        for it in collected:
            if self.equipment.add_item(it):
                self.game.all_sprites.remove(it)
                self.game.items.remove(it)

    def throw(self):
        """Throwing item from eq"""
        thrown = self.equipment.remove_item("active")
        if not thrown:
            return

        thrown.pos = vector(self.position.x + 80 * self.facing + 15 + WIDTH / 2, self.position.y - 50 + HEIGHT / 2)

        self.game.all_sprites.add(thrown)
        self.game.items.add(thrown)

    def update(self):
        """Update player position, check collisons, collect/throw items, handle keys pressed"""

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

        self.location.set(self.rect.x, self.rect.y)

        self.collect()
        self.held_item = self.equipment.get_active_item()

        # Sprawdzanie kolizji z boosterami
        self.check_collision_boosters()

        # To zostaje nadpisane, jeśli działa tło (background.py) w klasie tła @see class Background
        self.rect.midbottom = (self.position.x, self.position.y)

        self.key_actions(can_jump)

    def key_actions(self, can_jump):
        """Handle keys pressed"""
        # Zmiana wektorów przyspieszenia gracza, gdy wciśnięte przyciski poruszania
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.facing = -1
            self.acc.x = -PLAYER_MOVE["PLAYER_ACC"]
            self.standing = False
        elif keys[pygame.K_RIGHT]:
            self.facing = 1
            self.acc.x = PLAYER_MOVE["PLAYER_ACC"]
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
                    if self.mana_bar.decrease_mana(SPELL_COST[self.spell_ctrl]):
                        self.last_cast[self.spell_ctrl] = now_ctrl
                        self.spells.flag_ctrl = True
                        self.spells.last_ctrl = now_ctrl
                        if self.facing == 1:
                            cur_pos = vector(self.position.x, self.rect.centery + 10)
                        else:
                            cur_pos = vector(self.position.x - self.rect.width, self.rect.centery + 10)
                        # Prędkość pionowa pocisku po wystrzeleniu
                        speed_y = random.uniform(-0.2, 0.2)
                        if self.spell_ctrl == "fireball":
                            Fireball(self.game, cur_pos, speed_y, self.facing)
                        elif self.spell_ctrl == "frostbullet":
                            FrostBullet(self.game, cur_pos, speed_y, self.facing)

        # zmiana ataku podstawowego, gdy wciśnięty shift
        elif keys[pygame.K_LSHIFT]:
            now_shift = pygame.time.get_ticks()
            # Delay between swapping
            if now_shift - self.last_shift > 200:
                self.last_shift = now_shift
                if self.spell_ctrl is None:
                    self.spell_ctrl = "fireball"
                    self.spells.special += 1
                elif self.spell_ctrl == "fireball":
                    self.spell_ctrl = "frostbullet"
                    self.spells.special += 1
                else:
                    self.spell_ctrl = None
                    self.spells.special = 7

        # Tutaj w zaklęcie "uzbraja się" klawiszami 7, 8, 9, 0
        # lub tymi klawiszami automatycznie się wykonuje zaklęcie
        elif keys[pygame.K_7]:
            self.spell_key = self.spells.get_spell_at(0)
            self.execute_skill(0)
        elif keys[pygame.K_8]:
            self.spell_key = self.spells.get_spell_at(1)
            self.execute_skill(1)
        elif keys[pygame.K_9]:
            self.spell_key = self.spells.get_spell_at(2)
            self.execute_skill(2)
        elif keys[pygame.K_0]:
            self.spell_key = self.spells.get_spell_at(3)
            self.execute_skill(3)

    def execute_skill(self, number):
        """Casting or preparing full skills"""
        now_key = pygame.time.get_ticks()
        if now_key - self.last_cast[self.spell_key] > SPELL_DELAYS[self.spell_key]:
            self.spells.chosen = number
            # Skille rzucane od razu
            if self.spell_key in ["selfheal", "magicshield", "bard"]:
                if self.mana_bar.decrease_mana(SPELL_COST[self.spell_key]):
                    self.last_cast[self.spell_key] = now_key
                    self.spells.flag_key = True
                    self.spells.last_key = now_key
                    if self.spell_key == "selfheal":
                        SelfHeal(self.game)
                    elif self.spell_key == "magicshield":
                        MagicShield(self.game)
                    else:
                        Bard(self.game)
            # Skille rzucane ręcznie
            elif self.mana_bar.mana - SPELL_COST[self.spell_key] >= 0:
                self.spell_cast_ready = True

    def hit(self, attack):
        print(f"attack: {attack}")

    def heal(self, hp_value):
        return self.health_bar.increase_health(hp_value)


# Wywolanie akcji przedmiotu
# if keys[pygame.K_n]:
#            item = self.equipment.get_active_item()
#            if item and item.action():
#                item = self.equipment.remove_item("active")
