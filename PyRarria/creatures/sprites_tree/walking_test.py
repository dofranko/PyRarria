from creatures.physical_engine import *
from creatures.sprites_attributes import WALKING_TEST
from creatures.sprites_animations import WALKING_TEST_ANIMATION
from creatures.sprites_tree.walking_sprite import WalkingSprite
from settings import FPS

import math

ANIMATION = WALKING_TEST_ANIMATION
OBJECT = WALKING_TEST


class WalkingTest(WalkingSprite):

    animation = [ANIMATION["left"], ANIMATION["right"]]
    frames = ANIMATION["frames"]
    width = ANIMATION["width"]
    height = ANIMATION["height"]
    radius = min(width, height)
    animation_ticks = math.floor(FPS * ANIMATION["speed"])
    frame_ticks = math.ceil(FPS * ANIMATION["speed"] / ANIMATION["frames"])

    def __init__(self, x, y):
        super(WalkingTest, self).__init__(x, y)
        self.create(x, y, **OBJECT)

        # test
        # self.position = PVector(400, -500)
        self.is_enemy = False

    def update_forces(self, player, blocks):
        gravity(self)
        keep_on_platform(self, blocks)
        run_after(self, player)
        freeze(self)
        player_delete(self, player)
