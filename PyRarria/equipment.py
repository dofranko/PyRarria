import pygame
from settings import *
vec = pygame.math.Vector2

#Klasa, która tworzy ekwipunek i zarządza nim
class Equipment():
    def __init__(self, game, player, *, eq_size = 18):
        self.game = game
        self.active_tool_number = 1                 #Number aktualnie wybranego narzędzia
        self.base_x, self.base_y  = 5, 5            #Współrzędne (x, y) położenia eq
        self.base_width, self.base_height = 0,0     #Inicjowane również w funkcji create_eq_GUI()
        self.is_opened = False                      #Czy otwarty
        self.eq_size = eq_size                      #Rozmiar całego eq
        self.loaded_images = {}                     #Przechowywanie obrazków przedmiotów (żeby nie duplikować ich wczytywania)
        self.change_tool = None                     #Pomoc do swapowania przedmiotów
        self.base_eq = pygame.sprite.Group()        #Sprite eq 1-6
        self.extended_eq = pygame.sprite.Group()    #Sprite eq powyżej 6
        self.extra_sprites = pygame.sprite.Group()  #Sprite'y dodatkowe, takie jak przycisk czy suwak
        self.__create_eq_GUI()
        #Tablica przechowująca zebrane itemy gracza
        self.collected_items = [{} for i in range(self.eq_size)]
        #TODO do testów; wyrzucić potem PS TAK WYGLĄDA MINIMUM ATRYBUTÓW PRZEDMIOTU. 
        # PS (Moja -prymitywna- aktualna propozycja. Można zmieniać :P)
        self.collected_items[8] = {"name": "example_tool", "number": 1}
    
    #Stworzenie wyglądu eq    
    def __create_eq_GUI(self):
        eq_panel_image = pygame.image.load("resources/images/eq_square.png").convert_alpha()    #=====Tu można zmienić sprite===============
        self.base_width, self.base_height = eq_panel_image.get_rect().size
        for i in range(6):
            new_eq = pygame.sprite.Sprite()
            new_eq.image = eq_panel_image
            new_eq.rect = new_eq.image.get_rect()
            new_eq.rect.x, new_eq.rect.y = (self.base_x + i*self.base_width, self.base_y)
            self.base_eq.add(new_eq)
        for pos in range(6, self.eq_size):
            i = pos % 6
            j = pos // 6
            new_eq = pygame.sprite.Sprite()
            new_eq.image = eq_panel_image
            new_eq.rect = new_eq.image.get_rect()
            new_eq.rect.x, new_eq.rect.y = (self.base_x + i*self.base_width, self.base_y + j*self.base_height)
            self.extended_eq.add(new_eq)
        #Przycisk otwierania TODO =======Tu można zmienić sprite=======
        self.open_button = pygame.sprite.Sprite()
        self.open_button.image = pygame.image.load("resources/images/open_eq.png").convert_alpha() 
        self.open_button.rect = self.open_button.image.get_rect()
        self.open_button.rect.x =  5 + self.base_x + len(self.base_eq)*self.base_width
        self.open_button.rect.y = 5 + self.base_y
        self.extra_sprites.add(self.open_button)
        #Sprite pokazujący aktywny przedmiot TODO ==========Tu można zmienić sprite=========
        surface = pygame.Surface((self.base_width, 5)) 
        surface.fill(RED)
        self.active_tool = pygame.sprite.Sprite()
        self.active_tool.image = surface
        self.active_tool.rect = vec(self.base_x, 5) 
        self.extra_sprites.add(self.active_tool)
        
    def update(self):
        keys_pressed = pygame.key.get_pressed()
        keys_tab = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]
        for i, key in enumerate(keys_tab, 1):
            if keys_pressed[key]:
                self.active_tool_number = i
                break
        else:
            return
        self.active_tool.rect.x = self.base_x + self.base_width*(self.active_tool_number-1)
        
    def draw(self):
        #Rysowanie pierwszych 6 paneli (zawsze są pokazywane) i ekwipunku (jeśli jakiś jest)
        self.base_eq.draw(self.game.screen)
        for i in range(len(self.base_eq)):
             if self.collected_items[i]:
                self.game.screen.blit(self.get_image(self.collected_items[i]["name"]), (5 + self.base_x + i*self.base_width, 5 + self.base_y))
        #Rysowanie przycisku otwierania eq i znacznika aktywnego eq
        self.extra_sprites.draw(self.game.screen)
        #Rysowanie paneli i ekwipunku, gdy eq jest otwarte
        if self.is_opened:
            self.extended_eq.draw(self.game.screen)
            for pos in range(6, self.eq_size):
                i = pos % 6  #Położenie panelu na osi x
                j = pos // 6 #Położenie panelu na osi y
                if self.collected_items[pos]:
                    self.game.screen.blit(self.get_image(self.collected_items[pos]["name"]), 
                                            (5 + self.base_x + i*self.base_width, 5 + self.base_y + j*self.base_height))
                
    #Return: if item was added
    def add_item(self, new_item):
        for item in self.collected_items:
            if item and item["name"] == new_item["name"]:
                item["number"] += new_item["number"]
                return True
        for item in self.collected_items:
            if not bool(item): #if empty
                item = new_item
                return True
        return False #EQ is FULL
             
    #Usuwa (odejmuje liczbę) item. Można usunąć przez: 
    #1)Podanie "active" - usuwa aktualnie wybrany przedmiot
    #2)Podanie nazwy przedmiotu - usunie pierwszy
    #Jeszcze do rozbudowy
    def remove_item(self, item, number = 1):
        if item == "active":
            self.collected_items[self.active_tool_number-1]["number"] -= number
            if self.collected_items[self.active_tool_number-1]["number"] == 0:
                self.collected_items[self.active_tool_number-1].clear()
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
    
    #Return: atkualnie wybrany item        
    def get_active_item(self):
        return self.collected_items[self.active_tool_number-1]
    
    #Przechwycenie zdarzeń myszki: -otwarcie/zamknięcie eq; -zmiana pozycji przedmiotów
    # (wysyła main, ponieważ wywołanie kilka razy pobrania eventu myszki daje inne rezultaty)
    def handle_mouse(self, event):
        if event.button == 1: 
            mouse_pos = pygame.mouse.get_pos()
            if self.open_button.rect.collidepoint(mouse_pos):
                self.change_state()
                return
            if self.is_opened:
                for i, eq in enumerate(self.base_eq):
                    if eq.rect.collidepoint(mouse_pos):
                        self.change_positions(i)
                for i, eq in enumerate(self.extended_eq, 6):
                    if eq.rect.collidepoint(mouse_pos):
                        self.change_positions(i)
                        
    #Funkcja do zamiany eq miejscami        
    def change_positions(self, position):
        #Jeśli wybrano dopiero pierwszy item
        if self.change_tool == None:
            if self.collected_items[position]:
                self.change_tool = position
        else: #Swap items
            self.collected_items[self.change_tool], self.collected_items[position] = self.collected_items[position], self.collected_items[self.change_tool]
            self.change_tool = None

    #Metoda zwracająca obrazy z pamięci (cele optymalizacyjne, żeby nie powielać wczytywania obrazków)     
    def get_image(self, name):
        if name  not in self.loaded_images.keys():
            self.loaded_images[name] = pygame.image.load("resources/images/" + name + ".png").convert_alpha()
        return self.loaded_images[name]
