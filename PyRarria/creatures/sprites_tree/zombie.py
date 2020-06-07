from creatures.physical_engine import *
from creatures.sprites_attributes import ZOMBIE
from creatures.sprites_animations import ZOMBIE_ANIMATION
from creatures.sprites_tree.walking_sprite import WalkingSprite
from settings import FPS

import math

ANIMATION = ZOMBIE_ANIMATION
OBJECT = ZOMBIE


class Zombie(WalkingSprite):

    # static variables
    animation = [ANIMATION["left"], ANIMATION["right"]]
    frames = ANIMATION["frames"]
    width = ANIMATION["width"]
    height = ANIMATION["height"]
    radius = min(width, height)
    animation_ticks = math.floor(FPS * ANIMATION["speed"])
    frame_ticks = math.ceil(FPS * ANIMATION["speed"] / ANIMATION["frames"])

    def __init__(self, x, y):
        super(Zombie, self).__init__(x, y)
        self.create(x, y, **OBJECT)

    def apply_force(self, force):
        self.acceleration += force

    def update_forces(self, player, blocks):
        gravity(self)
        jump_from_platform(self, blocks)
        run_after(self, player)
        freeze(self)
