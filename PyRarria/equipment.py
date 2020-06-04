import pygame
from settings import *
from items import *
from copy import copy


# Klasa, która tworzy ekwipunek i zarządza nim
class Equipment:
    """A class representing equipement and holding items"""

    def __init__(self, game, player, *, eq_size=21):
        self.game = game
        self.active_tool_number = 0  # Number aktualnie wybranego narzędzia
        self.base_x, self.base_y = 5, 5  # Współrzędne (x, y) położenia eq
        self.base_width, self.base_height = 0, 0  # Inicjowane również w funkcji create_eq_GUI()
        self.is_opened = False  # Czy otwarty
        self.eq_size = eq_size  # Rozmiar całego eq
        self.loaded_images = {}  # Przechowywanie obrazków przedmiotów (żeby nie duplikować ich wczytywania)
        self.change_tool = None  # numer przenoszonego przedmiotu
        self.equipment_moving = False  # flaga do przenoszenia przedmiotu
        self.equipment = None  # przenoszony przedmiot
        self.eq_x = None  # współrzędne przenoszonego przedmiotu
        self.eq_y = None
        self.offset_x = None  # pomocnicze zmienne do przenoszenia
        self.offset_y = None
        self.font = pygame.font.SysFont("dejavusans", 15, 0, 0)
        self.armour_description = ["Drop a helmet here", "Drop a breastplate here", "Drop boots here"]
        self.base_eq = pygame.sprite.Group()  # Sprite eq 1-6
        self.extended_eq = pygame.sprite.Group()  # Sprite eq powyżej 6
        self.list_base_eq = []
        self.extra_sprites = []  # Sprite'y dodatkowe, takie jak przycisk czy suwak
        self.__create_eq_GUI()
        # Tablica przechowująca zebrane itemy gracza
        self.collected_items = [[] for i in range(self.eq_size)]
        # TODO do testów;
        self.collected_items[8] = [self.game.fabryka.create("kilof", 0, 0), self.game.fabryka.create("kilof", 0, 0)]

    def __create_eq_GUI(self):
        """"Create base eq gui"""
        # Podstawowe kwadraty eq (zarówno pierwsze 6 jak i rozwijane)
        self.eq_panel_image = pygame.image.load(IMAGES_LIST["eq_square"]).convert_alpha()
        self.base_width, self.base_height = self.eq_panel_image.get_rect().size
        for i in range(6):
            new_eq = pygame.sprite.Sprite()
            new_eq.image = copy(self.eq_panel_image)
            new_eq.rect = new_eq.image.get_rect()
            new_eq.rect.x, new_eq.rect.y = (self.base_x + i * self.base_width, self.base_y)
            self.list_base_eq.append(new_eq)
            self.base_eq.add(new_eq)
        for pos in range(6, self.eq_size - 3):
            i = pos % 6
            j = pos // 6
            new_eq = pygame.sprite.Sprite()
            new_eq.image = self.eq_panel_image
            new_eq.rect = new_eq.image.get_rect()
            new_eq.rect.x, new_eq.rect.y = (self.base_x + i * self.base_width, self.base_y + j * self.base_height)
            self.extended_eq.add(new_eq)
        for j in range(3):
            new_eq = pygame.sprite.Sprite()
            new_eq.image = self.eq_panel_image
            new_eq.rect = new_eq.image.get_rect()
            new_eq.rect.x, new_eq.rect.y = (15 * self.base_width - 20, 3 * self.base_height + 5 + j * self.base_height)
            self.extended_eq.add(new_eq)
        self.open_eq_word = self.font.render("Click to unroll your stuff", True, WHITE)
        self.bin_word = self.font.render("Drop to delete a item", True, WHITE)
        # Przycisk otwierania
        self.open_eq = pygame.sprite.Sprite()
        self.open_eq.image = pygame.image.load(IMAGES_LIST["open_eq"]).convert_alpha()
        self.open_eq.rect = self.open_eq.image.get_rect()
        self.open_eq.rect.x = 5 + self.base_x + len(self.base_eq) * self.base_width
        self.open_eq.rect.y = 5 + self.base_y
        # kosz
        self.bin = pygame.sprite.Sprite()
        self.bin_image = pygame.image.load(IMAGES_LIST["bin"]).convert_alpha()
        self.bin_image = pygame.transform.scale(self.bin_image, (40, 40))
        self.bin.rect = self.bin_image.get_rect()
        self.bin.rect.x = 5 + len(self.base_eq) * self.base_width
        self.bin.rect.y = 10 + self.base_height
        # armor
        self.list_armour = []
        for name in ["helmet", "breastplate", "boot"]:
            image = pygame.image.load(IMAGES_LIST[name]).convert_alpha()
            image = pygame.transform.scale(image, (35, 35))
            self.list_armour.append(image)

    def update(self):
        """Change active item in first row of eq"""
        keys_pressed = pygame.key.get_pressed()
        keys_tab = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]
        for i, key in enumerate(keys_tab):
            if keys_pressed[key]:
                self.active_tool_number = i
                break
        else:
            return

    def draw(self):
        """Draw all elements of eq"""
        # Rysowanie pierwszych 6 paneli (zawsze są pokazywane) i ekwipunku (jeśli jakiś jest)
        self.base_eq.draw(self.game.screen)
        for i in range(len(self.base_eq)):
            eq = self.list_base_eq[i]
            if self.collected_items[i]:
                if i != self.change_tool:  # nie rysujemy przedmiotu przenoszonego
                    if i == self.active_tool_number:  # podświetlenie przedmiotu
                        eq.image = copy(self.eq_panel_image)  # znika podświetlenie całego square
                        image = self.collected_items[i][0].image
                        image = pygame.transform.scale(image, (44, 44))
                        image.fill(GREEN, special_flags=pygame.BLEND_MAX)
                        self.game.screen.blit(image, (5 + self.base_x + i * self.base_width - 2, 5 + self.base_y - 2))

                    image = self.collected_items[i][0].image
                    image = pygame.transform.scale(image, (40, 40))
                    self.game.screen.blit(image, (5 + self.base_x + i * self.base_width, 5 + self.base_y))
                    if len(self.collected_items[i]) > 1:
                        num = str(len(self.collected_items[i]))
                        number = self.font.render(num, True, WHITE)
                        self.game.screen.blit(
                            number,
                            (
                                5 + self.base_x + i * self.base_width + image.get_width() - 7 * len(num),
                                5 + self.base_y + image.get_height() - 15,
                            ),
                        )
                elif i == self.active_tool_number:  # gdy przemieszczamy to podświetla
                    eq.image.fill(GREEN, special_flags=pygame.BLEND_MIN)
                elif self.active_tool_number is not None:
                    eq.image = copy(self.eq_panel_image)  # trzymając jakiś przedmiot można zmieniać
            elif i == self.active_tool_number:  # wybrany square bez przedmiotu
                eq.image.fill(GREEN, special_flags=pygame.BLEND_MIN)
            elif self.active_tool_number is not None:
                eq.image = copy(self.eq_panel_image)  # niewybrany square staje się normalny
        # Rysowanie przycisku otwierania eq
        self.game.screen.blit(self.open_eq.image, self.open_eq.rect)
        if self.open_eq.rect.collidepoint(pygame.mouse.get_pos()):
            x, y = pygame.mouse.get_pos()
            self.game.screen.blit(self.open_eq_word, (x - 15, y - 15))
        # Rysowanie paneli i ekwipunku, gdy eq jest otwarte
        if self.is_opened:
            self.extended_eq.draw(self.game.screen)
            for pos in range(6, self.eq_size - 3):
                i = pos % 6  # Położenie panelu na osi x
                j = pos // 6  # Położenie panelu na osi y
                if self.collected_items[pos]:
                    if pos != self.change_tool:  # nie rysujemy przedmiotu przenoszonego
                        image = self.collected_items[pos][0].image
                        image = pygame.transform.scale(image, (40, 40))
                        self.game.screen.blit(
                            image, (5 + self.base_x + i * self.base_width, 5 + self.base_y + j * self.base_height)
                        )
                        if len(self.collected_items[pos]) > 1:
                            num = str(len(self.collected_items[pos]))
                            number = self.font.render(num, True, WHITE)
                            self.game.screen.blit(
                                number,
                                (
                                    5 + self.base_x + i * self.base_width + image.get_width() - 7 * len(num),
                                    5 + self.base_y + j * self.base_height + image.get_height() - 15,
                                ),
                            )
            # Rysowanie kosza
            if self.equipment_moving:
                if self.bin.rect.collidepoint(pygame.mouse.get_pos()):
                    self.bin.image = pygame.transform.scale(self.bin_image, (42, 42))
                    self.game.screen.blit(self.bin.image, (self.bin.rect.x - 2, self.bin.rect.y - 2))
                    self.game.screen.blit(self.bin_word, (self.eq_x + 40, self.eq_y + 40))
                else:
                    self.bin.image = pygame.transform.scale(self.bin_image, (40, 40))
                    self.game.screen.blit(self.bin.image, self.bin.rect)

            # rysowanie zbroi
            for j in [18, 19, 20]:
                if self.collected_items[j]:
                    if j != self.change_tool:
                        image = self.collected_items[j][0].image
                        self.game.screen.blit(
                            image, (15 * self.base_width - 20, 3 * self.base_height + 5 + (j - 18) * self.base_height)
                        )
                        continue
                self.game.screen.blit(
                    self.list_armour[j - 18],
                    (15 * self.base_width - 13, 3 * self.base_height + 12 + (j - 18) * self.base_height),
                )

        # Rysowanie przenoszonego przedmiotu
        if self.equipment is not None:
            self.game.screen.blit(self.equipment, (self.eq_x, self.eq_y))
            num = str(len(self.collected_items[self.change_tool]))
            number = self.font.render(num, True, WHITE)
            if num != "1":
                self.game.screen.blit(
                    number,
                    (
                        self.eq_x + self.equipment.get_width() - 7 * len(num),
                        self.eq_y + self.equipment.get_height() - 15,
                    ),
                )
        elif self.is_opened:  # rysowanie opisów
            x, y = pygame.mouse.get_pos()
            i = None
            for k, eq in enumerate(self.base_eq):
                if eq.rect.collidepoint(pygame.mouse.get_pos()):
                    i = k
            for k, eq in enumerate(self.extended_eq, 6):
                if eq.rect.collidepoint(pygame.mouse.get_pos()):
                    i = k
            if i is not None and self.collected_items[i]:
                words = self.font.render(self.collected_items[i][0].description, True, WHITE)
                self.game.screen.blit(words, (x + 15, y + 15))
            elif i in [18, 19, 20]:
                words = self.font.render(self.armour_description[i - 18], True, WHITE)
                self.game.screen.blit(words, (x - 120, y - 15))

    def add_item(self, new_item):
        """Try to add item to eq. Return if item was added"""
        for item in self.collected_items:
            if item and item[0].name == new_item.name:
                item.append(new_item)
                return True
        for i in range(len(self.collected_items)):
            if not bool(self.collected_items[i]):  # if empty
                self.collected_items[i] = [new_item]
                return True
        return False  # EQ is FULL

    # Usuwa (odejmuje liczbę) item. Można usunąć przez:
    # 1)Podanie "active" - usuwa aktualnie wybrany przedmiot
    # 2)Podanie nazwy przedmiotu - usunie pierwszy
    # Jeszcze do rozbudowy
    def remove_item(self, item_name):
        """Try to remove item from eq. Return removed item"""
        if item_name == "active":
            if self.collected_items[self.active_tool_number]:
                active = self.collected_items[self.active_tool_number].pop(0)
                return active
        elif isinstance(item_name, Item):
            for el in self.collected_items:
                if el[0].name == item_name:
                    it = el.pop(0)
                    return it
        return None

    def open(self):
        """Open eq"""
        self.is_opened = True
        self.change_tool = None

    def close(self):
        """Close eq"""
        self.is_opened = False
        self.change_tool = None

    def change_state(self):
        """If opend close, if closed open"""
        if self.is_opened:
            self.close()
        else:
            self.open()

    # Return: atkualnie wybrany item
    def get_active_item(self):
        """Return actualy held item"""
        try:
            return self.collected_items[self.active_tool_number][0]
        except IndexError:
            return None

    # Przechwycenie zdarzeń myszki: -otwarcie/zamknięcie eq; -zmiana pozycji przedmiotów
    # (wysyła main, ponieważ wywołanie kilka razy pobrania eventu myszki daje inne rezultaty)
    def handle_mouse(self, event):
        """Handle mouse action (open/close eq, drag items)"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # sprawdza, czy to lewy przycisk
            if self.open_eq.rect.collidepoint(event.pos):
                self.change_state()
                return
            if self.is_opened:
                i = None
                for k, eq in enumerate(self.base_eq):
                    if eq.rect.collidepoint(event.pos) and self.collected_items[k]:
                        i = k
                for k, eq in enumerate(self.extended_eq, 6):
                    if eq.rect.collidepoint(event.pos) and self.collected_items[k]:
                        i = k
                if i is not None:
                    self.equipment_moving = True
                    self.equipment = pygame.transform.scale(self.collected_items[i][0].image, (40, 40))
                    if i < len(self.base_eq):
                        self.eq_x = 5 + self.base_x + i * self.base_width
                        self.eq_y = 5 + self.base_y
                    elif i < len(self.base_eq) + len(self.extended_eq):
                        k = i % 6  # Położenie na osi x
                        j = i // 6  # Położenie na osi y
                        self.eq_x = 5 + self.base_x + k * self.base_width
                        self.eq_y = 5 + self.base_y + j * self.base_height
                    else:  # armor
                        self.eq_x = 15 * self.base_width - 20
                        self.eq_y = 3 * self.base_height + 5 + (i - 18) * self.base_height
                    self.offset_x = self.eq_x - event.pos[0]
                    self.offset_y = self.eq_y - event.pos[1]
                    self.change_positions(i)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.equipment_moving:
                    self.equipment_moving = False
                    self.equipment = None
                    for i, eq in enumerate(self.base_eq):
                        if eq.rect.collidepoint(event.pos):
                            self.change_positions(i)
                    for i, eq in enumerate(self.extended_eq, 6):
                        if eq.rect.collidepoint(event.pos):
                            self.change_positions(i)
                    if self.bin.rect.collidepoint(event.pos):
                        self.collected_items[self.change_tool] = []
                    self.change_tool = None
        elif event.type == pygame.MOUSEMOTION:
            if self.equipment_moving:
                self.eq_x = event.pos[0] + self.offset_x
                self.eq_y = event.pos[1] + self.offset_y

    # Funkcja do zamiany eq miejscami
    def change_positions(self, position):
        """Swap positions of items in eq or set flag for moving item"""
        # Jeśli wybrano dopiero pierwszy item
        if self.change_tool is None:
            if self.collected_items[position]:
                self.change_tool = position
        else:  # Swap items
            # warunek
            # if self.collected_items[self.change_tool].name = 'armour' and
            self.collected_items[self.change_tool], self.collected_items[position] = (
                self.collected_items[position],
                self.collected_items[self.change_tool],
            )
            self.change_tool = None
