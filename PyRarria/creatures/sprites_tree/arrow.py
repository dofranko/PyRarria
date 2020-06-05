from creatures.sprites_attributes import ARROW
from creatures.sprites_animations import ARROW_ANIMATION
from creatures.sprites_tree.flying_sprite import FlyingSprite
from creatures.physical_engine import *
from creatures.test_global_settings import FPS

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

    def apply_force(self, force):
        force.limit(self.maxforce)
        self.acceleration += force

    def update_forces(self, player, platforms):
        gravity_bullet(self)
        edges_delete(self)
        platform_stop(self, platforms)

