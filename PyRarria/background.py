import pygame
from settings import *
vector = pygame.math.Vector2

class Background():
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.stages = []            #Lista dalszych planów tła
        #Main stage
        self.stage_width = 5000    #Szerokość całej planszy. TODO Można zmienić lub jakoś upłynnić np w settings.py
        self.start_scrolling_position = vector(WIDTH / 2, HEIGHT / 2)   #Póki co, position.y nie jest wykorzystywany
        self.main_image = pygame.image.load("resources/images/mv_bg.png").convert_alpha()
        self.main_stage = Stage(game, *self.main_image.get_rect().size, slowing_rate = 1, image = self.main_image)
        #Dalsze tła (liczba mnoga)
        stage_2 = Stage(game, *self.main_image.get_rect().size, image_source = "resources/images/mv_bg2.png", slowing_rate = 3)
        self.stages.append(stage_2)
        
    def update_player_and_rect_x(self):   
        #Jeśli gracz jest na lewym końcu mapy to nie przewijamy tła
        if self.player.position.x < self.start_scrolling_position.x: 
            self.player.rect.x = self.player.position.x
            self.main_stage.position.x = -self.start_scrolling_position.x
        #Jeśli gracz jest na prawym końcu mapy to nie przewijamy tła
        elif self.player.position.x > self.stage_width - self.start_scrolling_position.x: 
            self.player.rect.x = self.player.position.x - self.stage_width + WIDTH
        #Haha przewijane tło robi suuuuwu suwu
        else:
            #Tu ważne: w tym miejscu centrujemy player.rect - nie w jego klasie.
            self.player.rect.x = self.start_scrolling_position.x
            self.main_stage.position.x = -self.player.position.x
            
    def update_player_and_rect_y(self):
        #Pozycja gracza Y i sceny
        self.player.rect.y = self.start_scrolling_position.y
        self.main_stage.position.y = -self.player.position.y
        
    def update(self):
        #Pozycja gracza X i sceny:
        self.update_player_and_rect_x()
        self.update_player_and_rect_y()
        
        
        #Aktualizacja pozycji dalszych teł (dopełniacz liczby mnogiej ;-; )
        for stage in self.stages:
            stage.update(self.main_stage.position)
    
    def draw(self):
        #Jeśli tło będzie dobrze zrobione lub porządany będzie śmieszny efekt nakładania się obrazków, gdy nie ma tła, to usunąć
        self.game.screen.fill(BLACK)
        #Reversed, bo ostatnie dodane tło ma być 'na spodzie'
        for stage in reversed(self.stages):
            stage.draw()
            
        #Wyświetlenie głównego (przedniego) tła 
        self.main_stage.draw()
        
#Klasa teł    
class Stage():
    def __init__(self, game, background_width, background_height, *, image_source = None, slowing_rate = 3, image = None): 
        if image_source == None and image == None:
            raise NoImageProvidedError("Neither `image` nor `image_source` attribute provided.")
        self.game = game
        self.position = vector(0, 0)
        self.image = image
        if image_source != None:
            self.image = pygame.image.load(image_source).convert_alpha()
        self.width, self.height = self.image.get_rect().size
        self.slowing_rate = slowing_rate
        self.background_height = background_height
        self.background_width = background_width
        
    #Aktuaizacja pozycji (wywołane tylko dla dalszych teł)
    def update(self, main_stage_position):
        self.position = main_stage_position // self.slowing_rate
    
    #Rysowanie tła (jeśli wielkość obrazków jest conajmniej wielkości ekranu to chyba wszystkie przypadki rozpatrzone)
    def draw(self):
        relative_position = vector(self.position.x % self.background_width, self.position.y % self.background_height)
        self.game.screen.blit(self.image, (relative_position.x - self.background_width, relative_position.y - self.background_height))
        if relative_position.x < WIDTH:
            self.game.screen.blit(self.image, (relative_position.x, relative_position.y - self.background_height))
        if relative_position.y < HEIGHT:
            self.game.screen.blit(self.image, (relative_position.x, relative_position.y))  
        if relative_position.y < HEIGHT and relative_position.y < WIDTH:
            self.game.screen.blit(self.image, (relative_position.x - self.background_width, relative_position.y)) 
            
            
class NoImageProvidedError(Exception):
    pass
