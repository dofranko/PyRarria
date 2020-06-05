from PyRarria.creatures.physical_engine import *
from PyRarria.creatures.sprites_attributes import SHEEP
from PyRarria.creatures.sprites_animations import SHEEP_ANIMATION
from PyRarria.creatures.sprites_tree.arrow import Arrow
from PyRarria.creatures.sprites_tree.walking_sprite import WalkingSprite
from PyRarria.creatures.test_global_settings import FPS

import math

ANIMATION = SHEEP_ANIMATION
OBJECT = SHEEP

class Sheep(WalkingSprite):

    # static variables
    animation = [ANIMATION['left'], ANIMATION['right']]
    frames = ANIMATION['frames']
    width = ANIMATION['width']
    height = ANIMATION['height']
    radius = min(width, height)
    animation_ticks = math.floor(FPS * ANIMATION['speed'])
    frame_ticks = math.ceil(FPS * ANIMATION['speed'] / ANIMATION['frames'])

    def __init__(self, x, y):
        super(Sheep, self).__init__(x, y)
        self.create(x, y, **OBJECT)
