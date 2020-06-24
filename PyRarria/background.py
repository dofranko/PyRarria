import pygame
from settings import *

vector = pygame.math.Vector2


class Background:
    """A class for drawing background images"""

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.stages = []  # Lista dalszych planów tła
        # Main stage
        self.stage_width = MAP_WIDTH  # Szerokość całej planszy.
        self.start_scrolling_position = vector(0, 0)
        self.main_image = pygame.image.load(IMAGES_LIST["background"]["main"]).convert_alpha()
        self.main_stage = Stage(
            game, *self.main_image.get_rect().size, slowing_rate=1, image=self.main_image, y_offset=1000
        )
        # Dalsze tła (liczba mnoga)
        stage_2 = Stage(
            game,
            *self.main_image.get_rect().size,
            image_source=IMAGES_LIST["background"]["2"],
            slowing_rate=4,
            y_offset=1600,
        )
        stage_3 = Stage(
            game, *self.main_image.get_rect().size, image_source=IMAGES_LIST["background"]["3"], slowing_rate=5,
        )
        self.stages.append(stage_2)
        self.stages.append(stage_3)

    def update_player_and_rect_x(self):
        """Updating main stage position x and player rect x"""
        # Tu ważne: w tym miejscu centrujemy player.rect - nie w jego klasie.
        self.player.rect.x = self.start_scrolling_position.x + WIDTH / 2
        self.main_stage.position.x = -self.player.position.x

    def update_player_and_rect_y(self):
        """Updating main stage position y and player rect y"""
        # Pozycja gracza Y i sceny
        self.player.rect.y = self.start_scrolling_position.y + HEIGHT / 2
        self.main_stage.position.y = -self.player.position.y

    def update(self):
        """Update main stage's and player's positions"""
        # Pozycja gracza X i sceny:
        self.update_player_and_rect_x()
        self.update_player_and_rect_y()

        # Aktualizacja pozycji dalszych teł (dopełniacz liczby mnogiej ;-; )
        for stage in self.stages:
            stage.update(self.main_stage.position)

    def draw(self):
        """"Draw background"""
        # Reversed, bo ostatnie dodane tło ma być 'na spodzie'
        for stage in reversed(self.stages):
            stage.draw()

        # Wyświetlenie głównego (przedniego) tła
        self.main_stage.draw()


class Stage:
    """A class displaying stage of background"""

    def __init__(
        self, game, background_width, background_height, *, image_source=None, slowing_rate=3, image=None, y_offset=0
    ):
        if image_source is None and image is None:
            raise NoImageProvidedError("Neither `image` nor `image_source` attribute provided.")
        self.game = game
        self.position = vector(0, 0)
        self.image = image
        if image_source is not None:
            self.image = pygame.image.load(image_source).convert_alpha()
        self.width, self.height = self.image.get_rect().size
        self.slowing_rate = slowing_rate
        self.y_offset = y_offset
        self.background_height = background_height
        self.background_width = background_width

    # Aktuaizacja pozycji (wywołane tylko dla dalszych teł)
    def update(self, main_stage_position):
        """Update position of stage if it's not main stage"""
        self.position = main_stage_position // self.slowing_rate

    def draw(self):
        """Drawing stage"""
        """ """
        pos_x_tmp = self.position.x % self.width
        if pos_x_tmp > 0:
            pos_x_tmp -= self.width

        self.game.screen.blit(self.image, (pos_x_tmp, self.y_offset / self.slowing_rate + self.position.y))
        img = self.image
        for i in range(WIDTH):
            if pos_x_tmp + i * self.width > WIDTH:
                break
            self.game.screen.blit(
                img, (pos_x_tmp + i * self.width, self.y_offset / self.slowing_rate + self.position.y)
            )


class NoImageProvidedError(Exception):
    pass
