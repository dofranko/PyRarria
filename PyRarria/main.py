import pygame
import sys

from settings import *
from player import *
from equipment import *
from spells_icon import *
from background import *
from health_bar import *
from mana_bar import *
from items_factory import *
from boosters import *
from items.items_generator import *
from creatures.creatures_engine import CreaturesEngine
from creatures.vector import PVector
from map_generator import *

vector = pygame.math.Vector2


class Game:
    """Main class starting game"""

    def __init__(self):
        # Initialize game window
        pygame.init()
        # pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.pause = False
        self.creatures_engine = None

    def new_game(self):
        """Start new game"""
        # start a new game
        self.grid = {}
        generuj()

        # self.trees = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.boosters = pygame.sprite.Group()
        self.active_boosters = pygame.sprite.Group()
        self.magics = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.all_creatures = pygame.sprite.Group()
        self.arrows = pygame.sprite.Group()
        self.items_factory = Factory(self)
        self.equipment = Equipment(self)
        self.spells = Spells(self)
        self.health_bar = HealthBar(self)
        self.mana_bar = ManaBar(self)
        self.player = Player(self, self.equipment, self.health_bar, self.mana_bar, self.spells)
        self.background = Background(self, self.player)
        self.items_engine = ItemsEngine(self)
        self.main_position = PVector(*self.get_main_stage_position())
        self.last_main_position = PVector(*self.get_main_stage_position())
        self.creatures_engine = CreaturesEngine(self)

        create_world(self.grid, self.items_factory)

        self.waiting = True

        # test
        bacon = self.items_factory.create("bacon", 1750, 100)
        self.bacon = bacon
        # self.all_sprites.add(potato)
        self.items.add(bacon)

        # Tutaj testowanie dodawania boosterów
        position = vector(1193, 478)
        position2 = vector(1294, 487)
        position3 = vector(500, 170)
        position4 = vector(400, 10)
        position5 = vector(500, 470)
        position6 = vector(1400, 470)

        boost_test1 = TweeningBooster(self, position, "health")
        boost_test2 = TweeningBooster(self, position2, "mana")
        boost_test3 = PlayerSpeedBooster(self, position3)
        boost_test4 = DamageBooster(self, position4)
        boost_test5 = DefenseBooster(self, position5)
        boost_test6 = AccuracyBooster(self, position6)
        self.all_sprites.add(self.player)
        self.run()

    def run(self):
        """Run game in loop"""
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        """Call an update for every class that needs it"""
        # Game Loop - Update
        # make update() for every sprite (players/enemy)

        self.player.update()
        self.equipment.update()
        self.background.update()
        for blok in Item.get_neighbours(self.player.position, BLOCK_RENDER_DISTANCE, self.grid, do_collision=False):
            blok.update()
        # for tree in self.trees:
        #     tree.update()

        self.creatures_engine.update()
        self.health_bar.update()
        self.mana_bar.update()
        self.boosters.update()
        self.active_boosters.update()
        self.magics.update()
        self.explosions.update()
        self.items.update()
        self.items_engine.update()
        # self.blocks.update()

    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                self.waiting = False
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                or event.type == pygame.MOUSEBUTTONUP
                or event.type == pygame.MOUSEMOTION
            ):
                self.equipment.handle_mouse(event)
                self.spells.handle_mouse(event)
                self.player.handle_mouse(event)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.pause = True
            self.paused()

    def draw(self):
        """Call a draw for all classes that need it"""
        # Game Loop - draw
        # Kolejność ma znaczenie
        self.background.draw()
        self.creatures_engine.draw()

        for blok in Item.get_neighbours(self.player.position, BLOCK_RENDER_DISTANCE, self.grid, do_collision=False):
            blok.draw()
        self.all_sprites.draw(self.screen)
        self.player.draw()

        # for tree in self.trees:
        #     tree.draw()
        self.health_bar.draw()
        self.mana_bar.draw()
        self.spells.draw(self.screen)
        self.equipment.draw(self.screen)
        self.items.draw(self.screen)
        # żeby przenoszony itemik był widoczny, nic go nie ma przykrywać, więc rysuje się na końcu
        self.spells.draw_moving_item(self.screen)
        # *after* drawing everything, flip the display
        # #NieZmieniaćBoNieBędzieDziałaćINawetTwórcyNieWiedząCzemu
        pygame.display.flip()

    def show_start_screen(self):
        """Display starting screen"""
        waiting = True
        font = pygame.font.SysFont("dejavusans", 30, 0, 0)
        # TODO tutaj fancy grafika od naszego świrka graficznego
        image = pygame.image.load(IMAGES_LIST["start_screen"]).convert()
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
                self.screen.blit(loser, (int(WIDTH / 4), int(HEIGHT - 50)))
            pygame.display.flip()  # nie zadzieraj z tym przeciwnikiem
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                waiting = False

    def show_game_over_screen(self):
        """Display game over screen"""
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
        image = pygame.image.load(IMAGES_LIST["game_over_screen"]).convert()
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

    def paused(self):
        """Pause game and display pause screen"""
        large_text = pygame.font.SysFont("comicsansms", 115)
        text = large_text.render("Paused", True, (255, 255, 255))
        alpha_surface = pygame.Surface((WIDTH, HEIGHT))
        alpha_surface.fill((0, 0, 0))
        alpha_surface.set_alpha(120)
        self.screen.blit(alpha_surface, (0, 0))
        self.screen.blit(text, (WIDTH / 3, HEIGHT / 3))

        while self.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.pause = False

            self.screen.set_alpha(0)

            pygame.display.update()
            self.clock.tick(15)

    # Funkcja potrzebna platformom, żeby mogły dostosować swoją pozcję
    def get_main_stage_position(self):
        """Return main stage position - classes may need it for properly displaying on screen"""
        return self.background.main_stage.position + (WIDTH / 2, HEIGHT / 2)


if __name__ == "__main__":
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new_game()
        g.show_game_over_screen()

    pygame.quit()
