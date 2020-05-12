import pygame
import random
from settings import *
from platforms import *
from player import  *
from equipment import *
from background import *
vec = pygame.math.Vector2

class Game:
    def __init__(self):
        #Initialize game window
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.loaded_images = {}
        
    def new_game(self):
        # start a new game
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player(self)
        self.equipment = Equipment(self, self.player)
        self.background = Background(self, self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat, self)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.all_sprites.add(self.player)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        # make update() for every sprite (players/enemy)
        self.player.update()
        self.equipment.update()
        self.background.update()
        self.platforms.update()


    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.equipment.handle_mouse(event)

    def draw(self):
        # Game Loop - draw
        #Kolejność ma znaczenie
        self.background.draw()
        self.all_sprites.draw(self.screen)
        self.equipment.draw()
        # *after* drawing everything, flip the display
        # #NieZmieniaćBoNieBędzieDziałaćINawetTwórcyNieWiedząCzemu
        pygame.display.flip()
        

    def show_start_screen(self):
        # game splash/start screen
        print("Start Menu")

    def show_game_over_screen(self):
        # game over/continue
        print("Game Over")

    #Funkcja potrzebna platformom, żeby mogły dostosować swoją pozcję
    def get_main_stage_pos(self):
        #Try dla zasady, jakby coś się namieszało w kodzie
        try:
            return self.background.main_stage.pos
        except:
            print("sys.exc_info()[0]\n Continuing program")
            return vec(0, 0)
    
    
    
if __name__ == "__main__":
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new_game()
        g.show_game_over_screen()

    pygame.quit()