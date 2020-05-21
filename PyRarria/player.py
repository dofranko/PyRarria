# Sprite class for player
import pygame
from settings import *

vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    #Standardowo:   ^ position.x, position.y - pozycja względem całej mapy gry
    #               ^ rect.x, rect.y - pozycja względem monitora
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.position = vector(WIDTH / 2, 0 )
        self.vel = vector(0, 0)
        self.acc = vector(0, PLAYER_GRAV)
        
    
    def jump(self):
        # Skok tylko, jeśli stoi się na platformie
        self.vel.y = -20

    #Sprawdzenie kolizji (stania) od góry platform
    def check_collision_vertically(self):
        can_jump = False
        #Gdy porusza się w dół
        if self.vel.y > 0:
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False) #False -> don't remove from platforms
            if hits:
                new_position = min([hits[i].position.y for i in range(len(hits))])
                new_position += -(HEIGHT//2 + self.rect.height)   #SPECIAL ALIGN
                self.rect.y += new_position - self.position.y   #Cofnięcie na wcześniejszą pozycję (przed sprawdzaniem kolizji)
                self.position.y = new_position
                self.vel.y = 0
                can_jump = True
        #Gdy porusza się w górę
        elif -19 < self.vel.y < 0:
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False) #False -> don't remove from platforms
            if hits:
                new_position = max([hits[i].position.y + hits[i].rect.height + 1 for i in range(len(hits))])
                new_position += -(HEIGHT//2)   #SPECIAL ALIGN
                self.rect.y += new_position - self.position.y   #Cofnięcie na wcześniejszą pozycję (przed sprawdzaniem kolizji)
                self.position.y = new_position
                self.vel.y = 0 
        return can_jump
    
    def check_collision_horizontally(self):
        #Gdy porusza się w prawo
        if self.acc.x > 0:
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False) #False -> don't remove from platforms
            if hits:
                self.position.x = min([hits[i].position.x for i in range(len(hits))])
                self.position.x += -(WIDTH//2) - self.rect.width    #SPECIAL ALIGN
                self.acc.x = 0
        #Gdy porusza się w lewo
        elif self.acc.x < 0:
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False) #False -> don't remove from platforms
            if hits:
                self.position.x = max([hits[i].position.x + hits[i].rect.width for i in range(len(hits))])
                self.position.x +=  -WIDTH//2   #SPECIAL ALIGN
                self.acc.x = 0   
    
    def update(self):
        # Równania ruchu. Zabawa na własną odpowiedzialność :v
        self.vel.y += self.acc.y
        if self.vel.y > MAX_VEL_Y:
            self.vel.y = MAX_VEL_Y
           
        
        #Poruszenie się i sprawdzenie kolizji 
        self.position.y += self.vel.y + 0.5 * self.acc.y
        self.rect.y += self.vel.y + 0.5 * self.acc.y 
        can_jump = self.check_collision_vertically()
        
        self.position.x += self.acc.x
        self.rect.x += self.acc.x
        self.check_collision_horizontally()
        
        #To zostaje nadpisane, jeśli działa tło (background.py) w klasie tła @see class Background
        self.rect.midbottom = (self.position.x, self.position.y)
        
        #Zmiana wektorów przyspieszenia gracza, gdy wciśnięte przyciski poruszania
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -5
        elif keys[pygame.K_RIGHT]:
            self.acc.x = 5
        else:
            self.acc.x = 0
        if keys[pygame.K_UP] and can_jump:
            self.jump()

        #Stara funkcja tarcia po osi x. Prawdopodobnie już nie działa
        #self.acc.x += self.vel.x * PLAYER_FRICTION
                
