from PyRarria.creatures.physical_engine import *
from PyRarria.creatures.sprites_attributes import BAT
from PyRarria.creatures.sprites_animations import BAT_ANIMATION
from PyRarria.creatures.sprites_tree.flying_sprite import FlyingSprite
from PyRarria.creatures.test_global_settings import FPS

import math

ANIMATION = BAT_ANIMATION
OBJECT = BAT


class Bat(FlyingSprite):

    # static variables
    animation = [ANIMATION['left'], ANIMATION['right']]
    frames = ANIMATION['frames']
    width = ANIMATION['width']
    height = ANIMATION['height']
    radius = min(width, height)
    animation_ticks = math.floor(FPS * ANIMATION['speed'])
    frame_ticks = math.ceil(FPS * ANIMATION['speed'] / ANIMATION['frames'])

    def __init__(self, x, y):
        super(Bat, self).__init__(x, y)
        self.create(x, y, **OBJECT)

    def update_forces(self, player, platforms):
        track(self, player)
        edges_bounce(self)
        bounce_from_platform(self, platforms)