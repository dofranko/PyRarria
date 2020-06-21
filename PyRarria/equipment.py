import pygame
from settings import *
from items.item import *
from copy import copy

vector = pygame.math.Vector2


# Klasa, która tworzy ekwipunek i zarządza nim
class Equipment:
    """A class representing equipement and holding items"""

    def __init__(self, game, *, eq_size=18):
        self.game = game
        self.active_tool_number = 0  # Number aktualnie wybranego narzędzia
        self.base_x, self.base_y = 5, 5  # Współrzędne (x, y) położenia eq
        self.base_width, self.base_height = 0, 0  # Inicjowane również w funkcji create_eq_GUI()
        self.is_opened = False  # Czy otwarty
        self.eq_size = eq_size  # Rozmiar całego eq
        self.loaded_images = {}  # Przechowywanie obrazków przedmiotów (żeby nie duplikować ich wczytywania)
        self.change_tool = None  # numer przenoszonego przedmiotu
        self.item_moving = None  # przenoszony przedmiot
        self.eq = vector(-1, -1)  # współrzędne przenoszonego przedmiotu
        self.offset_x = None  # pomocnicze zmienne do przenoszenia
        self.offset_y = None
        self.font = pygame.font.SysFont("dejavusans", 15, 0, 0)
        self.armour_description = ["Drop a helmet here", "Drop a breastplate here", "Drop boots here"]
        self.base_eq = pygame.sprite.Group()  # Sprite eq 1-6
        self.extended_eq = pygame.sprite.Group()  # Sprite eq powyżej 6
        self.armor_eq = pygame.sprite.Group()  # Sprite armor eq
        self.extra_sprites = []  # Sprite'y dodatkowe, takie jak przycisk czy suwak
        self.__create_eq_GUI()
        # Tablica przechowująca zebrane itemy gracza
        self.collected_items = [[] for i in range(self.eq_size + 3)]  # +3 dla armoru
        # TODO do testów;
        self.collected_items[8] = [
            self.game.items_factory.create("pickaxe_diamond", 0, 0),
            self.game.items_factory.create("pickaxe_diamond", 0, 0),
        ]
        self.collected_items[1] = [
            self.game.items_factory.create("green_sword", 0, 0),
        ]
        self.collected_items[3] = [self.game.items_factory.create("black_helmet", 0, 0)]
        self.collected_items[4] = [self.game.items_factory.create("black_breastplate", 0, 0)]
        self.collected_items[5] = [self.game.items_factory.create("black_boots", 0, 0)]
        for _ in range(20):
            self.collected_items[2].append(self.game.items_factory.create("dirt", 0, 0))

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
            self.base_eq.add(new_eq)
        for pos in range(6, self.eq_size):
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
            new_eq.rect.x, new_eq.rect.y = (WIDTH - 3*BLOCK_SIZE - 20, 3 * self.base_height + 5 + j * self.base_height)
            self.armor_eq.add(new_eq)
        self.open_eq_word = self.font.render("Click to unroll your stuff", True, WHITE)
        self.bin_word = self.font.render("Drop to delete a item", True, WHITE)
        # Przycisk otwierania
        self.open_eq = pygame.sprite.Sprite()
        self.open_eq.image = pygame.image.load(IMAGES_LIST["open_eq"]).convert_alpha()
        self.open_eq.image = pygame.transform.scale(self.open_eq.image, (17, 17))
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
        # armour
        self.list_armour = []
        for name in ["helmet_icon_base", "breastplate_icon_base", "boots_icon_base"]:
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

    def draw(self, screen):
        """Draw all elements of eq"""
        self.draw_base_eq(screen)
        self.draw_eq_open(screen)
        self.draw_bin(screen)
        self.draw_armour(screen)
        self.draw_moving_item(screen)
        self.draw_item_description(screen)

    def draw_base_eq(self, screen):
        """Draw the visible part of equipment"""
        self.base_eq.draw(screen)
        for i in range(len(self.base_eq)):
            eq = self.base_eq.sprites()[i]
            if self.collected_items[i]:
                if i != self.change_tool:  # nie rysujemy przedmiotu przenoszonego
                    if i == self.active_tool_number:  # podświetlenie przedmiotu
                        eq.image = copy(self.eq_panel_image)  # znika podświetlenie całego square
                        item_image = self.collected_items[i][0].image
                        item_image = pygame.transform.scale(item_image, (44, 44))
                        item_image.fill(GREEN, special_flags=pygame.BLEND_MAX)
                        screen.blit(item_image, (5 + self.base_x + i * self.base_width - 2, 5 + self.base_y - 2))

                    item_image = self.collected_items[i][0].image
                    item_image = pygame.transform.scale(item_image, (40, 40))
                    screen.blit(item_image, (5 + self.base_x + i * self.base_width, 5 + self.base_y))
                    if len(self.collected_items[i]) > 1:
                        num = str(len(self.collected_items[i]))
                        number = self.font.render(num, True, WHITE)
                        screen.blit(
                            number,
                            (
                                5 + self.base_x + i * self.base_width + item_image.get_width() - 7 * len(num),
                                5 + self.base_y + item_image.get_height() - 15,
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
        screen.blit(self.open_eq.image, self.open_eq.rect)
        if self.open_eq.rect.collidepoint(pygame.mouse.get_pos()):
            x, y = pygame.mouse.get_pos()
            screen.blit(self.open_eq_word, (x - 15, y - 15))

    def draw_eq_open(self, screen):
        """Draw the rest of equipment when is open"""
        if self.is_opened:
            self.extended_eq.draw(screen)
            for pos in range(6, self.eq_size):
                i = pos % 6  # Położenie panelu na osi x
                j = pos // 6  # Położenie panelu na osi y
                if self.collected_items[pos]:
                    if pos != self.change_tool:  # nie rysujemy przedmiotu przenoszonego
                        item_image = self.collected_items[pos][0].image
                        item_image = pygame.transform.scale(item_image, (40, 40))
                        screen.blit(
                            item_image, (5 + self.base_x + i * self.base_width, 5 + self.base_y + j * self.base_height)
                        )
                        if len(self.collected_items[pos]) > 1:
                            num = str(len(self.collected_items[pos]))
                            number = self.font.render(num, True, WHITE)
                            screen.blit(
                                number,
                                (
                                    5 + self.base_x + i * self.base_width + item_image.get_width() - 7 * len(num),
                                    5 + self.base_y + j * self.base_height + item_image.get_height() - 15,
                                ),
                            )

    def draw_bin(self, screen):
        """Draw bin to remove items"""
        if self.item_moving is not None:
            if self.bin.rect.collidepoint(pygame.mouse.get_pos()):
                self.bin.image = pygame.transform.scale(self.bin_image, (42, 42))
                screen.blit(self.bin.image, (self.bin.rect.x - 2, self.bin.rect.y - 2))
                screen.blit(self.bin_word, (self.eq.x + 40, self.eq.y + 40))
            else:
                self.bin.image = pygame.transform.scale(self.bin_image, (40, 40))
                screen.blit(self.bin.image, self.bin.rect)

    def draw_armour(self, screen):
        """Draw armour like helmet, breastplate, boots"""
        if self.is_opened:
            self.armor_eq.draw(screen)
            armor_eq_pos = self.eq_size
            for j in [armor_eq_pos, armor_eq_pos + 1, armor_eq_pos + 2]:
                if self.collected_items[j]:
                    if j != self.change_tool:
                        item_image = self.collected_items[j][0].image
                        item_image = pygame.transform.scale(item_image, (40, 40))
                        screen.blit(
                            item_image,
                            (WIDTH - 3*BLOCK_SIZE - 15, 5 + 3 * self.base_height + 5 + (j - 18) * self.base_height),
                        )
                        continue
                screen.blit(
                    self.list_armour[j - 18],
                    (WIDTH - 3*BLOCK_SIZE - 13, 3 * self.base_height + 12 + (j - 18) * self.base_height),
                )

    def draw_moving_item(self, screen):
        """"Draw a moving item"""
        if self.item_moving is not None:  # rysowanie przenoszonego przedmiotu
            screen.blit(self.item_moving, (self.eq.x, self.eq.y))
            num = str(len(self.collected_items[self.change_tool]))
            number = self.font.render(num, True, WHITE)
            if num != "1":
                screen.blit(
                    number,
                    (
                        self.eq.x + self.item_moving.get_width() - 7 * len(num),
                        self.eq.y + self.item_moving.get_height() - 15,
                    ),
                )

    def draw_item_description(self, screen):
        """Draw a description of item"""
        if self.is_opened and self.item_moving is None:  # rysowanie opisów
            x, y = pygame.mouse.get_pos()
            i = None
            for k, eq in enumerate(self.base_eq):
                if eq.rect.collidepoint(pygame.mouse.get_pos()):
                    i = k
            for k, eq in enumerate(self.extended_eq, 6):
                if eq.rect.collidepoint(pygame.mouse.get_pos()):
                    i = k
            for k, eq in enumerate(self.armor_eq, self.eq_size):
                if eq.rect.collidepoint(pygame.mouse.get_pos()):
                    i = k
            armour_pos = self.eq_size
            if i is not None and self.collected_items[i] and i >= armour_pos:
                words = self.font.render(self.collected_items[i][0].description, True, WHITE)
                screen.blit(words, (x - 120, y - 15))
            elif i is not None and self.collected_items[i]:
                words = self.font.render(self.collected_items[i][0].description, True, WHITE)
                screen.blit(words, (x + 15, y + 15))
            elif i in [armour_pos, armour_pos + 1, armour_pos + 2]:
                words = self.font.render(self.armour_description[i - self.eq_size], True, WHITE)
                screen.blit(words, (x - 120, y - 15))

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
        """If opened close, if closed open"""
        if self.is_opened:
            self.close()
        else:
            self.open()

    # Return: atkualnie wybrany item
    def get_active_item(self):
        """Return actually held item"""
        try:
            return self.collected_items[self.active_tool_number][0]
        except IndexError:
            return None

    # zwraca elementy zbroi w specjalnych slotach
    def get_armour(self):
        """Return armour items which were chosen to be wear"""
        armour = []
        armour_position = self.eq_size
        if self.collected_items[armour_position]:
            armour.append(self.collected_items[armour_position][0])
        if self.collected_items[armour_position + 1]:
            armour.append(self.collected_items[armour_position + 1][0])
        if self.collected_items[armour_position + 2]:
            armour.append(self.collected_items[armour_position + 2][0])
        return armour

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
                for k, eq in enumerate(self.armor_eq, self.eq_size):
                    if eq.rect.collidepoint(event.pos) and self.collected_items[k]:
                        i = k
                if i is not None:
                    self.item_moving = pygame.transform.scale(self.collected_items[i][0].image, (40, 40))
                    if i < len(self.base_eq):
                        self.eq.x = 5 + self.base_x + i * self.base_width
                        self.eq.y = 5 + self.base_y
                    elif i < len(self.base_eq) + len(self.extended_eq):
                        k = i % 6  # Położenie na osi x
                        j = i // 6  # Położenie na osi y
                        self.eq.x = 5 + self.base_x + k * self.base_width
                        self.eq.y = 5 + self.base_y + j * self.base_height
                    else:  # armour
                        self.eq.x = 15 * self.base_width - 20
                        self.eq.y = 3 * self.base_height + 5 + (i - 18) * self.base_height
                    self.offset_x = self.eq.x - event.pos[0]
                    self.offset_y = self.eq.y - event.pos[1]
                    self.change_positions(i)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.item_moving is not None:
                    self.item_moving = None
                    for i, eq in enumerate(self.base_eq):
                        if eq.rect.collidepoint(event.pos):
                            self.change_positions(i)
                    for i, eq in enumerate(self.extended_eq, 6):
                        if eq.rect.collidepoint(event.pos):
                            self.change_positions(i)
                    for i, eq in enumerate(self.armor_eq, self.eq_size):
                        if eq.rect.collidepoint(event.pos):
                            self.change_positions(i)
                    if self.bin.rect.collidepoint(event.pos):
                        self.collected_items[self.change_tool] = []
                    self.change_tool = None
        elif event.type == pygame.MOUSEMOTION:
            if self.item_moving is not None:
                self.eq.x = event.pos[0] + self.offset_x
                self.eq.y = event.pos[1] + self.offset_y

    # Funkcja do zamiany eq miejscami
    def change_positions(self, position):
        """Swap positions of items in eq or set flag for moving item"""
        # Jeśli wybrano dopiero pierwszy item
        if self.change_tool is None:
            if self.collected_items[position]:
                self.change_tool = position
        else:  # Swap items
            # warunki by w armour była tylko zbroja
            armour_pos = self.eq_size
            flag = True
            # zmienianie itemsów wewnątrz slotów armour
            if self.change_tool in [armour_pos, armour_pos + 1, armour_pos + 2] and position in [
                armour_pos,
                armour_pos + 1,
                armour_pos + 2,
            ]:
                flag = False
            # zmienianie itemsów z armour na eq
            elif self.change_tool in [armour_pos, armour_pos + 1, armour_pos + 2]:
                flag = self.check_armour_condition(position, self.change_tool, armour_pos)
            # zmienianie itemsów z eq na armour
            elif position in [armour_pos, armour_pos + 1, armour_pos + 2]:
                flag = self.check_armour_condition(self.change_tool, position, armour_pos)
            if flag:
                self.collected_items[self.change_tool], self.collected_items[position] = (
                    self.collected_items[position],
                    self.collected_items[self.change_tool],
                )
            self.change_tool = None

    def check_armour_condition(self, new_index, index, armour_pos):
        """Check conditions to change items that are connected with armour slots"""
        flag = True
        if self.collected_items[new_index]:
            if index == armour_pos:
                if self.collected_items[new_index][0].get_type() != "helmet":
                    flag = False
            elif index == armour_pos + 1:
                if self.collected_items[new_index][0].get_type() != "breastplate":
                    flag = False
            elif index == armour_pos + 2:
                if self.collected_items[new_index][0].get_type() != "boots":
                    flag = False
        if flag:
            if self.collected_items[index]:
                self.collected_items[index][0].deactivate()
            if self.collected_items[new_index]:
                self.collected_items[new_index][0].activate()
        return flag
