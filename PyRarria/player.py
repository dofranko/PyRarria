# Sprite class for player
import pygame
from settings import *

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    #Standardowo:   ^ pos.x, pos.y - pozycja względem całej mapy gry
    #               ^ rect.x, rect.y - pozycja względem monitora
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, 0 )
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
    
    def jump(self, hits):
        # Skok tylko, jeśli stoi się na platformie
        # PS przekazuję skoki wyliczone wcześniej, bo:
        # 1) performance, 2)! bez tego działało beznadziejnie
        if hits:
            self.vel.y = -20

    #Sprawdzenie kolizji (stania) od góry platform
    def check_collision_ON_platform(self):
        hits = []
        if self.vel.y > 0:
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False) #False -> don't remove from platforms
            if hits:
                self.pos.y = min([hits[i].pos.y for i in range(len(hits))])
                self.pos.y += - (HEIGHT//2 + self.rect.height) + 2 
                # +2 to taki align, żeby nie było śmiesznego telepania ze spadaniem
                self.vel.y = 0
        return hits
    
    def update(self):
        # Równania ruchu. Zabawa na własną odpowiedzialność :v
        self.vel.x += self.acc.x
        self.vel.y += self.acc.y
        if self.vel.y > MAX_VEL_Y:
            self.vel.y = MAX_VEL_Y
        self.pos.x += self.acc.x
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.acc.y = PLAYER_GRAV
        
        
        #Sprawdzenie kolizji oraz ruchów
        keys = pygame.key.get_pressed()
        hits = self.check_collision_ON_platform()
        if keys[pygame.K_LEFT]:
            self.acc.x = -5
        elif keys[pygame.K_RIGHT]:
            self.acc.x = 5
        else:
            self.acc.x = 0
        if keys[pygame.K_UP]:
            self.jump(hits)

        #Stara funkcja tarcia po osi x. Prawdopodobnie już nie działa
        #self.acc.x += self.vel.x * PLAYER_FRICTION
        
        self.rect.midbottom = (self.pos.x, self.pos.y)
        
