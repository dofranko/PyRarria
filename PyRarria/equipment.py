import pygame
from settings import *



# Klasa, która tworzy ekwipunek i zarządza nim
class Equipment:
    def __init__(self, game, player, *, eq_size=18):
        self.game = game
        self.active_tool_number = 1  # Number aktualnie wybranego narzędzia
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
        self.base_eq = pygame.sprite.Group()  # Sprite eq 1-6
        self.extended_eq = pygame.sprite.Group()  # Sprite eq powyżej 6
        self.extra_sprites = pygame.sprite.Group()  # Sprite'y dodatkowe, takie jak przycisk czy suwak
        self.__create_eq_GUI()
        # Tablica przechowująca zebrane itemy gracza
        self.collected_items = [{} for i in range(self.eq_size)]
        # TODO do testów; wyrzucić potem PS TAK WYGLĄDA MINIMUM ATRYBUTÓW PRZEDMIOTU.
        # PS (Moja -prymitywna- aktualna propozycja. Można zmieniać :P)
        self.collected_items[8] = {"name": "example_tool", "number": 12}
        self.collected_items[9] = {"name": "example_tool_2", "number": 3}

    # Stworzenie wyglądu eq
    def __create_eq_GUI(self):
        eq_panel_image = pygame.image.load(
            "resources/images/eq_square.png").convert_alpha()  # =====Tu można zmienić sprite===============
        self.base_width, self.base_height = eq_panel_image.get_rect().size
        for i in range(6):
            new_eq = pygame.sprite.Sprite()
            new_eq.image = eq_panel_image
            new_eq.rect = new_eq.image.get_rect()
            new_eq.rect.x, new_eq.rect.y = (self.base_x + i * self.base_width, self.base_y)
            self.base_eq.add(new_eq)
        for pos in range(6, self.eq_size):
            i = pos % 6
            j = pos // 6
            new_eq = pygame.sprite.Sprite()
            new_eq.image = eq_panel_image
            new_eq.rect = new_eq.image.get_rect()
            new_eq.rect.x, new_eq.rect.y = (self.base_x + i * self.base_width, self.base_y + j * self.base_height)
            self.extended_eq.add(new_eq)
        # Przycisk otwierania TODO =======Tu można zmienić sprite=======
        self.open_button = pygame.sprite.Sprite()
        self.open_button.image = pygame.image.load("resources/images/open_eq.png").convert_alpha()
        self.open_button.rect = self.open_button.image.get_rect()
        self.open_button.rect.x = 5 + self.base_x + len(self.base_eq) * self.base_width
        self.open_button.rect.y = 5 + self.base_y
        self.extra_sprites.add(self.open_button)

    def update(self):
        keys_pressed = pygame.key.get_pressed()
        keys_tab = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]
        for i, key in enumerate(keys_tab, 1):
            if keys_pressed[key]:
                self.active_tool_number = i
                break
        else:
            return
        
    def draw(self):
        # Rysowanie pierwszych 6 paneli (zawsze są pokazywane) i ekwipunku (jeśli jakiś jest)
        self.base_eq.draw(self.game.screen)
        for i in range(len(self.base_eq)):
            if self.collected_items[i]:
                if i != self.change_tool:  # nie rysujemy przedmiotu przenoszonego
                    if i + 1 == self.active_tool_number:    # podświetlenie przedmiotu
                        image = self.get_image(self.collected_items[i]["name"])
                        image = pygame.transform.scale(image, (43, 43))
                        image.fill(GREEN, special_flags=pygame.BLEND_MAX)
                        self.game.screen.blit(image, (5 + self.base_x + i * self.base_width - 2, 5 + self.base_y - 2))
                    image = self.get_image(self.collected_items[i]["name"])
                    self.game.screen.blit(image, (5 + self.base_x + i * self.base_width, 5 + self.base_y))
                    if self.collected_items[i].get("number") > 1:
                        num = str(self.collected_items[i].get("number"))
                        number = self.font.render(num, True, WHITE)
                        self.game.screen.blit(number, (5 + self.base_x + i * self.base_width + image.get_width() -
                                                       7 * len(num), 5 + self.base_y + image.get_height() - 15))
        # Rysowanie przycisku otwierania eq i znacznika aktywnego eq
        self.extra_sprites.draw(self.game.screen)
        # Rysowanie paneli i ekwipunku, gdy eq jest otwarte
        if self.is_opened:
            self.extended_eq.draw(self.game.screen)
            for pos in range(6, self.eq_size):
                i = pos % 6  # Położenie panelu na osi x
                j = pos // 6  # Położenie panelu na osi y
                if self.collected_items[pos]:
                    if pos != self.change_tool:  # nie rysujemy przedmiotu przenoszonego
                        image = self.get_image(self.collected_items[pos]["name"])
                        self.game.screen.blit(image, (5 + self.base_x + i * self.base_width,
                                                      5 + self.base_y + j * self.base_height))
                        if self.collected_items[pos].get("number") > 1:
                            num = str(self.collected_items[pos].get("number"))
                            number = self.font.render(num, True, WHITE)
                            self.game.screen.blit(number, (5 + self.base_x + i * self.base_width + image.get_width() -
                                                           7 * len(num), 5 + self.base_y +
                                                           j * self.base_height + image.get_height() - 15))
        # Rysowanie przenoszonego przedmiotu

        if self.equipment is not None:
            self.game.screen.blit(self.equipment, (self.eq_x, self.eq_y))
            num = str(self.collected_items[self.change_tool].get("number"))
            number = self.font.render(num, True, WHITE)
            self.game.screen.blit(number, (self.eq_x + self.equipment.get_width() - 7 * len(num),
                                           self.eq_y + self.equipment.get_height() - 15))

    # Return: if item was added
    def add_item(self, new_item):
        for item in self.collected_items:
            if item and item["name"] == new_item["name"]:
                item["number"] += new_item["number"]
                return True
        for item in self.collected_items:
            if not bool(item):  # if empty
                item = new_item
                return True
        return False  # EQ is FULL

    # Usuwa (odejmuje liczbę) item. Można usunąć przez:
    # 1)Podanie "active" - usuwa aktualnie wybrany przedmiot
    # 2)Podanie nazwy przedmiotu - usunie pierwszy
    # Jeszcze do rozbudowy
    def remove_item(self, item, number=1):
        if item == "active":
            self.collected_items[self.active_tool_number - 1]["number"] -= number
            if self.collected_items[self.active_tool_number - 1]["number"] == 0:
                self.collected_items[self.active_tool_number - 1].clear()
        elif type(item) == str:
            for el in self.collected_items:
                if el["name"] == item:
                    el["number"] -= number
                    if el["number"] == 0:
                        el.clear()
                    break

    def open(self):
        self.is_opened = True
        self.change_tool = None

    def close(self):
        self.is_opened = False
        self.change_tool = None

    def change_state(self):
        if self.is_opened:
            self.close()
        else:
            self.open()

    # Return: atkualnie wybrany item
    def get_active_item(self):
        return self.collected_items[self.active_tool_number - 1]

    # Przechwycenie zdarzeń myszki: -otwarcie/zamknięcie eq; -zmiana pozycji przedmiotów
    # (wysyła main, ponieważ wywołanie kilka razy pobrania eventu myszki daje inne rezultaty)
    def handle_mouse(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1):  # sprawdza, czy to lewy przycisk
            if self.open_button.rect.collidepoint(event.pos):
                self.change_state()
                return
            if self.is_opened:
                i = None
                for k, eq in enumerate(self.base_eq):
                    if (eq.rect.collidepoint(event.pos) and
                            self.collected_items[k]):
                        i = k
                for k, eq in enumerate(self.extended_eq, 6):
                    if (eq.rect.collidepoint(event.pos) and
                            self.collected_items[k]):
                        i = k
                if i is not None:
                    self.equipment_moving = True
                    self.equipment = self.get_image(self.collected_items[i]["name"])
                    if i < 6:
                        self.eq_x = 5 + self.base_x + i * self.base_width
                        self.eq_y = 5 + self.base_y
                    else:
                        k = i % 6  # Położenie na osi x
                        j = i // 6  # Położenie na osi y
                        self.eq_x = 5 + self.base_x + k * self.base_width
                        self.eq_y = 5 + self.base_y + j * self.base_height
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
                    self.change_tool = None
        elif event.type == pygame.MOUSEMOTION:
            if self.equipment_moving:
                self.eq_x = event.pos[0] + self.offset_x
                self.eq_y = event.pos[1] + self.offset_y

    # Funkcja do zamiany eq miejscami
    def change_positions(self, position):
        # Jeśli wybrano dopiero pierwszy item
        if self.change_tool is None:
            if self.collected_items[position]:
                self.change_tool = position
        else:  # Swap items
            self.collected_items[self.change_tool], self.collected_items[position] = self.collected_items[position], \
                                                                                     self.collected_items[
                                                                                         self.change_tool]
            self.change_tool = None

    # Metoda zwracająca obrazy z pamięci (cele optymalizacyjne, żeby nie powielać wczytywania obrazków)
    def get_image(self, name):
        if name not in self.loaded_images.keys():
            image = pygame.image.load("resources/images/" + name + ".png").convert_alpha()
            image = pygame.transform.scale(image, (40, 40))
            self.loaded_images[name] = image
        return self.loaded_images[name]

