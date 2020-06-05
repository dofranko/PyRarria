from creatures.sprites_attributes import BIRD
from creatures.sprites_animations import BIRD_ANIMATION
from creatures.sprites_tree.flying_sprite import FlyingSprite
from settings import FPS

import math



ANIMATION = BIRD_ANIMATION
OBJECT = BIRD


class Bird(FlyingSprite):

    # static variables
    animation = [ANIMATION["left"], ANIMATION["right"]]
    frames = ANIMATION["frames"]
    width = ANIMATION["width"]
    height = ANIMATION["height"]
    radius = min(width, height)
    animation_ticks = math.floor(FPS * ANIMATION["speed"])
    frame_ticks = math.ceil(FPS * ANIMATION["speed"] / ANIMATION["frames"])

    def __init__(self, x, y):
        super(Bird, self).__init__(x, y)
        self.create(x, y, **OBJECT)
