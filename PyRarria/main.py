import pygame
import random
import sys
from settings import *
from platforms import *
from player import  *
from equipment import *
from background import *
from health_mana_bar import *
vector = pygame.math.Vector2

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
        self.health_bar = Health_bar(self)
        self.mana_bar = Mana_bar(self)
        self.waiting = True
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
        self.health_bar.update()
        self.mana_bar.update()


    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                self.waiting = False
                
            if (event.type == pygame.MOUSEBUTTONDOWN
                 or event.type == pygame.MOUSEBUTTONUP 
                   or event.type == pygame.MOUSEMOTION):
                self.equipment.handle_mouse(event)

    def draw(self):
        # Game Loop - draw
        #Kolejność ma znaczenie
        self.background.draw()
        self.all_sprites.draw(self.screen)
        self.equipment.draw()
        self.health_bar.draw()
        self.mana_bar.draw()
        # *after* drawing everything, flip the display
        # #NieZmieniaćBoNieBędzieDziałaćINawetTwórcyNieWiedząCzemu
        pygame.display.flip()
        

    def show_start_screen(self):
        waiting = True
        font = pygame.font.SysFont("dejavusans", 30, 0, 0)
        # TODO tutaj fancy grafika od naszego świrka graficznego
        image = pygame.image.load("resources/images/random_start.jpg").convert()
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))

        counter = 0  # migotanie napisu
        loser = font.render("Press ENTER to start the game", True, (255, 255, 255))
        while waiting:
            self.clock.tick(FPS)
            self.screen.blit(image, (0, 0))
            if counter < 40:
                counter += 1
            else:
                if counter < 150:
                    counter += 1
                else:
                    counter = 0
                self.screen.blit(loser, (WIDTH / 4, HEIGHT - 50))
            pygame.display.flip()  # nie zadzieraj z tym przeciwnikiem
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                waiting = False

    def show_game_over_screen(self):
        if not self.waiting:  # gdy wyłączamy grę, w pętli running wykona się jeszcze ta funkcja
            return
        alpha_surface = pygame.Surface((WIDTH, HEIGHT))  # background
        alpha_surface.fill((0, 0, 0))  # czarny background
        alpha_surface.set_alpha(0)  # przezroczysty, czarny background
        for alpha in range(60):  # stopniowo zwiększamy alpha
            alpha_surface.set_alpha(alpha)
            self.screen.blit(alpha_surface, (0, 0))
            font = pygame.font.SysFont("dejavusans", 3 * alpha, 0, 10)
            loser = font.render("YOU LOST", True, (255, 0, 0))
            self.screen.blit(loser, ((WIDTH / 2) - 6 * alpha, (HEIGHT / 2) - 10 * alpha))
            pygame.display.flip()  # nie zadzieraj z tym przeciwnikiem
            pygame.time.delay(50)
        image = pygame.image.load("resources/images/index.png").convert()
        image = pygame.transform.scale(image, (500, 500))
        self.screen.blit(image, (WIDTH / 5, 0))
        font = pygame.font.SysFont("dejavusans", 30, 0, 0)
        counter = 0  # przez jakiś czas napis czarny, przez jakiś czas czerwony, bo tak
        while self.waiting:
            self.clock.tick(FPS)
            if counter < 40:
                counter += 1
                loser = font.render("Press p to play again or q to quit the game", True, (0, 0, 0))
            else:
                if counter < 150:
                    counter += 1
                else:
                    counter = 0
                loser = font.render("Press p to play again or q to quit the game", True, (255, 0, 0))
            self.screen.blit(loser, (WIDTH / 7, HEIGHT - 100))
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                self.waiting = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_q]:
                    self.waiting = False
                    self.running = False

    #Funkcja potrzebna platformom, żeby mogły dostosować swoją pozcję
    def get_main_stage_position(self):
        #Try dla zasady, jakby coś się namieszało w kodzie
        try:
            return self.background.main_stage.position
        except:
            print(f"{sys.exc_info()}[0]\n Continuing program with values (0,0)")
            return vector(0, 0)
    
    
    
if __name__ == "__main__":
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new_game()
        g.show_game_over_screen()

    pygame.quit()