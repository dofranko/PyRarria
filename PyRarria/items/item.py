import math
import pygame

from os import path
from settings import *
from creatures.vector import PVector


class Item(pygame.sprite.Sprite):
    """A class representing item (on map or held in eq)"""

    items_loaded_images = {}

    def __init__(self, x, y, info, game, do_scale=True):
        pygame.sprite.Sprite.__init__(self)

        self.name = info.name
        self.description = info.description
        self.variety = info.variety
        self.angle = info.angle

        self.game = game
        self.damage = 5
        self.env_damage = 1
        self.durability = 100000
        self.range = 60

        self.vel_y = 0
        self.acc_y = 0

        self.image = self.load_image(self.name)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if do_scale:
            Item.scale_item(self, BLOCK_SIZE // 1.6)

        self.position = PVector(x, y)

    def check_collision(self):
        """Check collision (only to down)"""
        if self.vel_y > 0:
            hits = pygame.sprite.spritecollide(self, Item.get_neighbours(self.position, (5, 5), self.game.grid), False)
            if hits:
                self.position.y = min([(hits[i].position.y - self.rect.height) for i in range(len(hits))])
                self.vel_y = 0

    def falling(self):
        """If needed - fall"""
        self.check_collision()
        self.acc_y = PLAYER_MOVE["PLAYER_GRAV"]
        self.vel_y += self.acc_y
        if self.vel_y != 0:
            self.position.y += self.vel_y + 0.5 * self.acc_y

    def get_state(self):
        """Get if item is held by player or dropped on map"""
        if self in self.game.items:
            return "lying"
        if self == self.game.player.held_item:
            return "held"
        return "eq"

    def rot_center(self, image, angle):
        """Rotate item in hand"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def update(self):
        """Update item position"""
        main_stage_pos = self.game.get_main_stage_position()
        self.rect.x = self.position.x + main_stage_pos.x
        self.rect.y = self.position.y + main_stage_pos.y

        if self.get_state() == "lying":
            self.falling()

    # tylko dla itemu trzymanego przez playera
    def draw_on_player(self):
        """Draw item on player when held by player"""
        rot = self.rot_center(self.image, self.angle)
        player_width = self.game.player.rect.width
        player_height = self.game.player.rect.height
        align_x = 2 * player_width // 3
        rot = pygame.transform.scale(rot, (round(player_width * 2 / 3), round(player_height * 2 / 3)))
        if self.game.player.facing == -1:
            rot = pygame.transform.flip(rot, True, False)
            align_x = -player_width // 3
        obr_rect = rot.get_rect()
        obr_rect.x = self.game.player.rect.x + align_x
        obr_rect.y = self.game.player.rect.y + player_width // 3
        self.game.screen.blit(rot, obr_rect)

    def get_type(self):
        return self.variety

    # implementowane przez podklasy
    def action(self, mouse_pos, player):
        """By default it makes a little damage and a little env_damage in low range"""
        if math.hypot(mouse_pos[0] - player.rect.center[0], mouse_pos[1] - player.rect.center[1]) <= self.range:
            damaged = False
            for creature in self.game.all_creatures:
                if creature.rect.collidepoint(mouse_pos):
                    creature.hit(player, self.damage)
                    damaged = True
                    break
            else:
                position = Item.get_mouse_position_on_map(player, mouse_pos)
                blok_pos = PVector(*Item.cursor_to_grid(position.x, position.y))
                for block in Item.get_neighbours(blok_pos, (3, 3), self.game.grid, noncollidable_objects=True):
                    if block.rect.collidepoint(mouse_pos):
                        block.hit(self.env_damage)
                        damaged = True
                        break
            if damaged:
                self.durability -= 1
            if self.durability <= 0:
                return True
        return False

    def load_image(self, name):
        if name not in Item.items_loaded_images.keys():
            Item.items_loaded_images[name] = pygame.image.load(IMAGES_LIST[self.name]).convert_alpha()
        return Item.items_loaded_images[name]

    @staticmethod
    def get_neighbours(start_point, depth, grid, noncollidable_objects=False):
        pos = Item.cursor_to_grid(start_point.x, start_point.y)
        neighbours = []
        for i in range(-depth[0], depth[0] + 1):
            for j in range(-depth[1], depth[1] + 1):
                try:
                    blok = grid[(BLOCK_SIZE * i + pos[0], BLOCK_SIZE * j + pos[1])]
                except KeyError:
                    continue
                if blok:
                    neighbours.append(blok)
        if not noncollidable_objects:
            return [bl for bl in neighbours if bl.name not in NON_COLLISION_OBJECTS]
        return neighbours

    @staticmethod
    def cursor_to_grid(x, y):
        grid_x = (x // BLOCK_SIZE) * BLOCK_SIZE
        grid_y = (y // BLOCK_SIZE) * BLOCK_SIZE
        return (int(grid_x), int(grid_y))

    @staticmethod
    def scale_item(to_scale_object, size=BLOCK_SIZE // 1.6):
        """scales image when placed or destroyed"""
        to_scale_object.image = pygame.transform.scale(to_scale_object.image, (int(size), int(size)))
        X = to_scale_object.rect.x
        Y = to_scale_object.rect.y
        to_scale_object.rect = to_scale_object.image.get_rect()
        to_scale_object.rect.x = X
        to_scale_object.rect.y = Y

    @staticmethod
    def get_mouse_position_on_map(player, mouse_pos):
        mouse_pos = PVector(mouse_pos[0], mouse_pos[1])
        return PVector(player.position.x, player.position.y) + mouse_pos - PVector(WIDTH / 2, HEIGHT / 2)
