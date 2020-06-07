from creatures.sprites_attributes import ARROW
from creatures.sprites_animations import ARROW_ANIMATION
from creatures.sprites_tree.flying_sprite import FlyingSprite
from creatures.physical_engine import *
from settings import FPS

import math

ANIMATION = ARROW_ANIMATION
OBJECT = ARROW


class Arrow(FlyingSprite):

    # static variables
    animation = [ANIMATION["left"], ANIMATION["right"]]
    frames = ANIMATION["frames"]
    width = ANIMATION["width"]
    height = ANIMATION["height"]
    radius = min(width, height)
    animation_ticks = math.floor(FPS * ANIMATION["speed"])
    frame_ticks = math.ceil(FPS * ANIMATION["speed"] / ANIMATION["frames"])

    def __init__(self, x, y):
        super(Arrow, self).__init__(x, y)
        self.create(x, y, **OBJECT)
        self.rect = pg.rect.Rect(0, 0, self.radius, self.radius)

    def update(self, player, platforms, map_position, items_factory):
        # dead
        if self.hp <= 0:
            self.die(items_factory)
            return

        # arrow hits the target
        if self.is_target:
            self.hp -= 1

        # alive
        self.update_forces(player, blocks)
        self.move(map_position)

    def bite(self, player):
        if self.is_enemy and self.rect.colliderect(player):
            if self.bite_count > 0:
                self.bite_count -= 1
            else:
                direction = -1
                if self.position.x < player.position.x:
                    direction = 1
                player.hit(self.damage, direction)
                self.bite_count = 10000
                self.is_target = True

    def die(self, items_factory):
        self.kill()

    def update_forces(self, player, platforms):
        gravity_bullet(self)
        edges_delete(self)
        if platform_stop(self, platforms):
            self.is_target = True
