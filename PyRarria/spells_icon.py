import pygame
from settings import *


class Spells:
    """Class displaying icons and information about spells (only displaying, not casting)"""

    def __init__(self, game):
        self.game = game
        self.spells = []
        self.name_spells = [
            "smallfire",
            "smallthunder",
            "boulder",
            "magicshield",
            "selfheal",
            "bard",
            "freeze",
            "blank",
            "fireball",
            "frostbullet",
        ]
        self.description = [
            "Opis zaklęcia smallfire",
            "Opis zaklęcia smallthunder",
            "Opis zaklęcia boulder",
            "Opis zaklęcia magicshield",
            "Opis zaklęcia selfheal",
            "Opis zaklęcia bard",
            "Opis zaklęcia freeze",
            "Press Shift to change",
            "Opis zaklęcia fireball",
            "Opis zaklęcia frostbullet",
        ]
        self.chosen = None
        self.change_spell = None
        self.special = 7  # numer skilla, który zmienia się na shift
        self.flag_ctrl = False  # flaga czy ctrl został wciśnięty
        self.last_ctrl = 0  # kiedy został wciśnięty ctrl
        self.flag_key = False  # flaga czy key został wciśnięty
        self.last_key = 0  # analogicznie 7 8 9 0
        # tworzenie obrazków zaklęć
        for name in self.name_spells:
            image = pygame.image.load(IMAGES_LIST[name]).convert_alpha()
            image = pygame.transform.scale(image, (30, 30))
            self.spells.append(image)
        self.size = 30
        self.offset_x = None
        self.offset_y = None
        self.spell_x = None
        self.spell_y = None
        self.spell_moving = False
        self.spell = None
        self.sprites_list = []
        self.special_slot = []
        self.create_sprites()
        self.font = pygame.font.SysFont("comicsansms", 18)

    def create_sprites(self):
        """Create base icons"""
        for i, image in enumerate(self.spells[:4]):
            new_spell = pygame.sprite.Sprite()
            new_spell.image = image
            new_spell.rect = new_spell.image.get_rect()
            new_spell.rect.x, new_spell.rect.y = (7 * 50 + i * (self.size + 3), 5)
            self.sprites_list.append(new_spell)
        for pos, image in enumerate(self.spells[4:-3], 0):
            i = pos % 6
            j = pos // 6
            new_spell = pygame.sprite.Sprite()
            new_spell.image = image
            new_spell.rect = new_spell.image.get_rect()
            new_spell.rect.x, new_spell.rect.y = (7 * 50 + i * (self.size + 3), 40 + j * (self.size + 3))
            self.sprites_list.append(new_spell)
        for image in self.spells[-3:]:
            new_spell = pygame.sprite.Sprite()
            new_spell.image = image
            new_spell.rect = new_spell.image.get_rect()
            new_spell.rect.x, new_spell.rect.y = (11 * 50, 5)
            self.special_slot.append(new_spell)

    def draw(self, screen):
        """Draw icons"""
        for i, spell in enumerate(self.sprites_list[:4]):  # iterowanie po skillach, które można wybrać
            if i != self.change_spell or not self.spell_moving:  # nie rysujemy przenoszonego spella
                if i == self.chosen:
                    if self.flag_key:
                        now_key = pygame.time.get_ticks()
                        if now_key - self.last_key > 100:  # by było widać jednorazowe podświetlenie
                            self.chosen = None
                            self.flag_key = False
                    tmp = pygame.transform.scale(spell.image, (35, 35))
                    tmp.fill(GREEN, special_flags=pygame.BLEND_MAX)
                    screen.blit(tmp, (7 * 50 + i * (self.size + 3) - 2.5, 5 - 2.5))
                screen.blit(spell.image, spell.rect)
                # wyświetlanie braku możliwości wybrania skilla
                self.draw_blocking_time(spell, i, screen)
        for i, spell in enumerate(self.sprites_list[4:], 4):  # itercja po pozostałych skillach
            if i != self.change_spell or not self.spell_moving:
                screen.blit(spell.image, spell.rect)
                # wyświetlanie braku możliwości wybrania skilla
                self.draw_blocking_time(spell, i, screen)
        now_ctrl = pygame.time.get_ticks()
        if now_ctrl - self.last_ctrl > 100:  # by było widać jednorazowe podświetlenie
            self.flag_ctrl = False
        if self.flag_ctrl and self.special != 7:  # podświetlenie specjalnego slotu
            tmp = pygame.transform.scale(self.spells[self.special], (35, 35))
            tmp.fill(GREEN, special_flags=pygame.BLEND_MAX)
            screen.blit(tmp, (11 * 50 - 2.5, 5 - 2.5))
        screen.blit(self.special_slot[self.special - 7].image, (11 * 50, 5))  # specjalny slot
        self.draw_description(screen)

    def draw_blocking_time(self, spell, i, screen):
        """Draw numbers showing remaining time to unblock spell"""
        last_cast = self.game.player.last_cast[self.name_spells[i]]
        block_time = SPELL_DELAYS[self.name_spells[i]]
        now_time = pygame.time.get_ticks()
        if now_time - last_cast <= block_time:
            time_to_end = (last_cast + block_time - now_time) // 1000 + 1
            text = self.font.render(str(time_to_end), True, WHITE)
            tmp = pygame.transform.scale(spell.image, (30, 30))
            tmp.fill(GRAY, special_flags=pygame.BLEND_MIN)
            screen.blit(tmp, spell.rect)
            screen.blit(text, (spell.rect.x + 15 - len(str(time_to_end) * 3), spell.rect.y + 10))

    def draw_description(self, screen):
        """Draw description of spell"""
        for i, spell in enumerate(self.sprites_list):
            if spell.rect.collidepoint(pygame.mouse.get_pos()):
                x, y = pygame.mouse.get_pos()
                desc = self.font.render(self.description[i], True, WHITE)
                screen.blit(desc, (x + 15, y + 15))
        image = self.special_slot[self.special - 7]
        if image.rect.collidepoint(pygame.mouse.get_pos()):
            x, y = pygame.mouse.get_pos()
            desc = self.font.render(self.description[self.special], True, WHITE)
            screen.blit(desc, (x + 15, y + 15))

    def draw_moving_item(self, screen):
        """Draw moving spell"""
        if self.spell_moving:
            screen.blit(self.spell, (self.spell_x, self.spell_y))

    def handle_mouse(self, event):
        """Handle swaping spells"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, spell in enumerate(self.sprites_list):
                    if spell.rect.collidepoint(event.pos):
                        if i != self.chosen:
                            self.spell_moving = True  # można przenosić tylko niepodświetlone
                            self.spell = spell.image
                            if i < 4:
                                self.spell_x = 7 * 50 + i * (self.size + 3)
                                self.spell_y = 5
                            else:
                                pos = i - 4  # 6 wyrównanie
                                k = pos % 6  # Położenie na osi x
                                j = pos // 6  # Położenie na osi y
                                self.spell_x = 7 * 50 + k * (self.size + 3)
                                self.spell_y = 40 + j * (self.size + 3)
                            self.offset_x = self.spell_x - event.pos[0]
                            self.offset_y = self.spell_y - event.pos[1]
                            self.change_positions(i)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.spell_moving:
                    self.spell_moving = False
                    self.spell = None
                    for i, spell in enumerate(self.sprites_list):
                        if spell.rect.collidepoint(event.pos):
                            self.change_positions(i)
                    self.change_spell = None
        elif event.type == pygame.MOUSEMOTION:
            if self.spell_moving:
                self.spell_x = event.pos[0] + self.offset_x
                self.spell_y = event.pos[1] + self.offset_y

    def change_positions(self, position):
        """Method to swap two spells"""
        # Jeśli wybrano dopiero pierwszy item
        if self.change_spell is None:
            if self.spells[position]:
                self.change_spell = position
        elif position != self.change_spell and position != self.chosen:  # Swap items
            tmp = self.sprites_list[self.change_spell].rect.x
            tmp2 = self.sprites_list[self.change_spell].rect.y
            self.sprites_list[self.change_spell].rect.x = self.sprites_list[position].rect.x
            self.sprites_list[self.change_spell].rect.y = self.sprites_list[position].rect.y
            self.sprites_list[position].rect.x, self.sprites_list[position].rect.y = tmp, tmp2
            self.sprites_list[self.change_spell], self.sprites_list[position] = (
                self.sprites_list[position],
                self.sprites_list[self.change_spell],
            )
            tmp3 = self.name_spells[self.change_spell]
            self.name_spells[self.change_spell] = self.name_spells[position]
            self.name_spells[position] = tmp3
            tmp4 = self.description[self.change_spell]
            self.description[self.change_spell] = self.description[position]
            self.description[position] = tmp4
            self.change_spell = None
            if position == self.chosen:
                self.chosen = None

    def get_spell_at(self, number):
        """Return spells at position @number"""
        return self.name_spells[number]
