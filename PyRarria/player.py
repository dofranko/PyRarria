# Sprite class for player
import pygame
import random

from map_generator import *
from settings import *
from bullet_spells import *
from fast_spells import *
from items.item import Item
from items.block import *
from creatures.vector import PVector


vector = PVector


class Player(pygame.sprite.Sprite):
    """Sprite class for player"""

    # Standardowo:   ^ position.x, position.y - pozycja względem całej mapy gry
    #               ^ rect.x, rect.y - pozycja względem monitora
    def __init__(self, game, equipment, health_bar, mana_bar, spells):
        super().__init__()
        poz_tmp = surface[int(len(surface) / 2)]
        poz_y = poz_tmp[1] * BLOCK_SIZE - 3 * BLOCK_SIZE
        poz_x = poz_tmp[0] * BLOCK_SIZE
        self.game = game
        self.equipment = equipment
        self.image = pygame.image.load(IMAGES_LIST["player"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, ((int(BLOCK_SIZE * 1.5)), (int(BLOCK_SIZE * 2.5))))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, 0)
        self.position = vector(poz_x, poz_y)
        self.vel = vector(0, 0)
        self.acc = vector(0, PLAYER_MOVE["PLAYER_GRAV"])
        self.mask = pygame.mask.from_surface(self.image)
        self.facing = 1
        self.q_trigger = False
        self.held_item = None
        self.last_shift = 0
        self.spell_cast_ready = False
        self.double_jump = False  # wskazuje czy można skoczyć w powietrzu
        self.next_jump = False
        self.last_jump = None

        self.health_bar = health_bar
        self.mana_bar = mana_bar
        self.spells = spells

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

        # Zaklęcia przypisane do klawisza
        self.spell_ctrl = None
        self.spell_key = None

    def jump(self):
        """Player jumps (only if on platform) - change velocity y value"""
        self.vel.y = PLAYER_MOVE["JUMP_VEL"]

    def _get_close_blocks(self):
        return Item.get_neighbours(self.position, (5, 5), self.game.grid)

    # Sprawdzenie kolizji (stania) od góry platform
    def check_collision_vertically(self):
        """Check collistion up/down and move if collided
            return if player standing on platform
        """
        can_jump = False
        # Gdy porusza się w dół
        if self.vel.y > 0:
            hits = pygame.sprite.spritecollide(self, self._get_close_blocks(), False)
            if hits:
                new_position = min([hits[i].position.y for i in range(len(hits))])
                new_position += -(self.rect.height)  # SPECIAL ALIGN
                # Cofnięcie na wcześniejszą pozycję (przed sprawdzaniem kolizji)
                self.rect.y += new_position - self.position.y
                self.position.y = new_position
                self.vel.y = 0
                can_jump = True

        # Gdy porusza się w górę
        elif self.vel.y < 0:
            hits = pygame.sprite.spritecollide(self, self._get_close_blocks(), False)
            if hits:
                new_position = max([hits[i].position.y + hits[i].rect.height + 1 for i in range(len(hits))])
                # new_position += -(HEIGHT // 2)  # SPECIAL ALIGN
                # Cofnięcie na wcześniejszą pozycję (przed sprawdzaniem kolizji)
                self.rect.y += new_position - self.position.y
                self.position.y = new_position
                self.vel.y = 0
        return can_jump

    def check_collision_horizontally(self):
        """Check collistion left/right and move if collided"""
        # Gdy porusza się w prawo
        if self.vel.x > 0:
            hits = pygame.sprite.spritecollide(
                self, self._get_close_blocks(), False
            )  # False -> don't remove from blocks
            if hits:
                new_position = min([hits[i].position.x for i in range(len(hits))])
                new_position += -self.rect.width  # SPECIAL ALIGN
                self.rect.x += new_position - self.position.x
                self.position.x = new_position
                self.vel.x = 0
        # Gdy porusza się w lewo
        elif self.vel.x < 0:
            hits = pygame.sprite.spritecollide(
                self, self._get_close_blocks(), False
            )  # False -> don't remove from blocks
            if hits:
                new_position = max([hits[i].position.x + hits[i].rect.width for i in range(len(hits))])
                self.rect.x += new_position - self.position.x
                self.position.x = new_position
                # self.position.x += -WIDTH // 2  # SPECIAL ALIGN
                self.vel.x = 0

    # Sprawdzanie kolizji boosterów (prostokątów gracza i ich)
    def check_collision_boosters(self):
        """Check if player collected boosters"""
        hits = pygame.sprite.spritecollide(self, self.game.boosters, False)
        for hit in hits:
            if pygame.sprite.collide_mask(self, hit):
                hit.apply_boost()

    def handle_mouse(self, event):
        self.handle_mouse_cast_spell(event)
        self.execute_item_action(event)

    def execute_item_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            item = self.equipment.get_active_item()
            if item and item.action(event.pos, self):
                item = self.equipment.remove_item("active")

    def handle_mouse_cast_spell(self, event):
        """Handle mouse spell casting and cast if needed"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.spell_cast_ready:
                # Castowanie tylko na potwory
                for sprite in self.game.all_creatures:
                    if sprite.rect.collidepoint(event.pos):
                        if self.mana_bar.decrease_mana(SPELL_COST[self.spell_key] - PLAYER_VALUES["MANA_REDUCTION"]):
                            self.last_cast[self.spell_key] = pygame.time.get_ticks()
                            cur_pos = vector(event.pos[0], event.pos[1])
                            # for ex Freeze(self.game, cur_pos)
                            SpellName = eval(f"{SPELLS_NORMAL_NAME[self.spell_key]}")
                            thrown_spell = SpellName(self.game, cur_pos)
                            sprite.hit(self, thrown_spell.damage)
                            self.spells.chosen = None
                            self.spell_cast_ready = False
                        break

    def collect(self):
        """Adding item to eq that was collided"""
        collected = pygame.sprite.spritecollide(self, self.game.items, False)
        for it in collected:
            if self.equipment.add_item(it):
                self.game.items.remove(it)

    def throw(self):
        """Throwing item from eq"""
        thrown = self.equipment.remove_item("active")
        if not thrown:
            return

        thrown.position = vector(self.position.x + 80 * self.facing + 15, self.position.y - 50)
        Item.scale_item(thrown, BLOCK_SIZE // 1.6)
        self.game.items.add(thrown)

    def scale(self, item, rozm):
        """Scales image when placed or destroyed"""
        self.image = pygame.transform.scale(self.image, (rozm, rozm))
        X = self.rect.x
        Y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = X
        self.rect.y = Y

    def update(self):
        """Update player position, check collisons, collect/throw items, handle keys pressed"""
        # Równania ruchu. Zabawa na własną odpowiedzialność :v
        self.vel.y += self.acc.y
        if self.vel.y > PLAYER_MOVE["MAX_VEL_Y"]:
            self.vel.y = PLAYER_MOVE["MAX_VEL_Y"]

        # Poruszenie się i sprawdzenie kolizji
        self.position.y += self.vel.y + 0.5 * self.acc.y
        self.rect.y += self.vel.y + 0.5 * self.acc.y
        can_jump = self.check_collision_vertically()

        self.acc.x += self.vel.x * PLAYER_MOVE["FRICTION"]
        self.vel.x += self.acc.x

        self.position.x += self.vel.x + 0.5 * self.acc.x
        self.rect.x += self.vel.x + 0.5 * self.acc.x
        self.check_collision_horizontally()

        if abs(self.acc.x) < 1e-5:
            self.acc.x = 0
        if abs(self.vel.x) < 1e-5:
            self.vel.x = 0

        self.collect()
        self.held_item = self.equipment.get_active_item()

        # Sprawdzanie kolizji z boosterami
        self.check_collision_boosters()
        # To zostaje nadpisane, jeśli działa tło (background.py) w klasie tła @see class Background
        # self.rect.midbottom = (self.position.x, self.position.y)

        self.key_actions(can_jump)

    def draw(self, screen):
        player_sprite = self.image
        if self.game.player.facing == -1:
            player_sprite = pygame.transform.flip(player_sprite, True, False)
        
        screen.blit(player_sprite, (self.rect.x, self.rect.y))
        for armour in reversed(self.equipment.get_armour()):
            armour.get_dressed()
        if self.held_item:
            self.held_item.draw_on_player()

    def key_actions(self, can_jump):
        """Handle keys pressed"""
        keys = pygame.key.get_pressed()
        self.make_moves(keys, can_jump)
        self.skill_key_actions(keys)

    def make_moves(self, keys, can_jump):
        # Zmiana wektorów przyspieszenia gracza, gdy wciśnięte przyciski poruszania
        if keys[pygame.K_LEFT]:
            self.facing = -1
            self.acc.x = -PLAYER_MOVE["PLAYER_ACC"]
        elif keys[pygame.K_RIGHT]:
            self.facing = 1
            self.acc.x = PLAYER_MOVE["PLAYER_ACC"]
        else:
            self.acc.x = 0
        if keys[pygame.K_UP]:
            if can_jump:
                self.jump()
                self.next_jump = True
                self.last_jump = pygame.time.get_ticks()
            elif self.double_jump and self.next_jump:
                now = pygame.time.get_ticks()
                if now - self.last_jump > 150:
                    self.jump()
                    self.next_jump = False
        if keys[pygame.K_q]:
            if not self.q_trigger:
                self.throw()
            self.q_trigger = True
        else:
            self.q_trigger = False

    def skill_key_actions(self, keys):
        # Wystrzeliwanie magicznych pocisków, gdy wciśnięty ctrl
        if keys[pygame.K_LCTRL]:
            if self.spell_ctrl is not None:
                now_ctrl = pygame.time.get_ticks()
                if now_ctrl - self.last_cast[self.spell_ctrl] > SPELL_DELAYS[self.spell_ctrl]:
                    if self.mana_bar.decrease_mana(SPELL_COST[self.spell_ctrl] - PLAYER_VALUES["MANA_REDUCTION"]):
                        self.last_cast[self.spell_ctrl] = now_ctrl
                        self.spells.flag_ctrl = True
                        self.spells.last_ctrl = now_ctrl
                        if self.facing == 1:
                            cur_pos = vector(self.position.x + self.rect.width - 3, self.position.y + 10)
                        else:
                            cur_pos = vector(self.position.x - self.rect.width, self.position.y + 10)
                        # Prędkość pionowa pocisku po wystrzeleniu
                        value = PLAYER_VALUES["ACCURACY"]
                        speed_y = random.uniform(-0.2 / value, 0.2 / value)
                        # For ex. FireBall(self.game, cur_pos, speed_y, self.facing)
                        SpellName = eval(f"{SPELLS_NORMAL_NAME[self.spell_ctrl]}")
                        SpellName(self.game, cur_pos, speed_y, self.facing)

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
            if self.mana_bar.mana - (SPELL_COST[self.spell_key] - PLAYER_VALUES["MANA_REDUCTION"]) >= 0:
                self.spells.chosen = number
                # Skille rzucane od razu
                if self.spell_key in ["selfheal", "magicshield", "bard"]:
                    self.mana_bar.decrease_mana(SPELL_COST[self.spell_key] - PLAYER_VALUES["MANA_REDUCTION"])
                    self.last_cast[self.spell_key] = now_key
                    self.spells.flag_key = True
                    self.spells.last_key = now_key
                    SpellName = eval(f"{SPELLS_NORMAL_NAME[self.spell_key]}")
                    SpellName(self.game)
                # Skille rzucane ręcznie
                else:
                    self.spell_cast_ready = True

    def hit(self, attack, direction):
        real_attack = attack - PLAYER_VALUES["DEFENCE"]
        if real_attack > 0:
            self.health_bar.decrease_health(real_attack)
            force = real_attack / HEART_VALUE * 4
            self.push_away(direction, force=force)

    def heal(self, hp_value):
        return self.health_bar.increase_health(hp_value)

    def push_away(self, direction, push_vel_x=14, push_vel_y=12, force=1):
        if force < 0.4:
            force = 0.4
        self.vel.y = -push_vel_y * force
        self.vel.x = push_vel_x * direction * force


# Wywolanie akcji przedmiotu
# if keys[pygame.K_n]:
#            item = self.equipment.get_active_item()
#            if item and item.action(mouse_pos, pself.position):
#                item = self.equipment.remove_item("active")
