import pygame
import random

from settings import *
from boosters import *
from items_factory import *

vector = pygame.math.Vector2

FREQUENCIES = {
    "damage_booster": 0.8,
    "defense_booster": 0.8,
    "speed_booster": 0.8,
    "accuracy_booster": 0.8,
    "heart": 0.8,
    "star": 0.8,
    "random_item": 0.2,
}

SPAWN_DISTANCE = vector(WIDTH * 1.2, HEIGHT * 1.2)
BASE_LATENCY = 3000  # x/1000 = sec
BASE_RANDOM_LATENCY = 500


class ItemsEngine:
    def __init__(self, game):

        # window, clock, main position
        self.game = game
        self.window = game.screen

        self.last_spawn = {}
        for key in FREQUENCIES.keys():
            self.last_spawn[key] = pygame.time.get_ticks()
        # map, player, arrows
        self.grid = game.grid
        self.player = game.player

        self.blank_image = pygame.image.load(IMAGES + "blank.png").convert_alpha()
        self.blank_image = pygame.transform.scale(self.blank_image, (50, 50))

    def update(self):
        actual_time = pygame.time.get_ticks()
        for name, time in self.last_spawn.items():
            if actual_time - time > BASE_LATENCY:
                self.last_spawn[name] = actual_time + BASE_LATENCY + random.random() * BASE_RANDOM_LATENCY
                if random.random() < FREQUENCIES[name]:
                    self.spawn(name)

    def spawn(self, name):
        position = vector(
            random.randint(-SPAWN_DISTANCE.x, SPAWN_DISTANCE.x) + self.player.position.x,
            random.randint(-SPAWN_DISTANCE.y, SPAWN_DISTANCE.y) + self.player.position.y,
        )

        blank = pygame.sprite.Sprite()
        blank.image = self.blank_image
        main_stage_position = self.game.get_main_stage_position()
        blank.rect = blank.image.get_rect()
        blank.rect.x, blank.rect.y = position + main_stage_position
        if pygame.sprite.spritecollide(blank, Item.get_neighbours(blank.rect, (5, 5), self.grid), False):
            blank.kill()
            return
        blank.rect.y += 50
        if not pygame.sprite.spritecollide(blank, Item.get_neighbours(blank.rect, (5, 5), self.grid), False):
            blank.kill()
            return
        blank.kill()
        if name == "heart":
            item = TweeningBooster(self.game, position, "health")
        elif name == "star":
            item = TweeningBooster(self.game, position, "mana")
        elif name == "speed_booster":
            item = PlayerSpeedBooster(self.game, position)
        elif name == "damage_booster":
            item = DamageBooster(self.game, position)
        elif name == "defense_booster":
            item = DefenseBooster(self.game, position)
        elif name == "accuracy_booster":
            item = AccuracyBooster(self.game, position)
        elif name == "random_item":
            return
