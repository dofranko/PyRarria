from PyRarria.creatures.physical_engine import *
from PyRarria.creatures.sprites_attributes import WALKING_TEST
from PyRarria.creatures.sprites_animations import WALKING_TEST_ANIMATION
from PyRarria.creatures.sprites_tree.walking_sprite import WalkingSprite
from PyRarria.creatures.test_global_settings import FPS

import math

ANIMATION = WALKING_TEST_ANIMATION
OBJECT = WALKING_TEST

class WalkingTest(WalkingSprite):

    animation = [ANIMATION['left'], ANIMATION['right']]
    frames = ANIMATION['frames']
    width = ANIMATION['width']
    height = ANIMATION['height']
    radius = min(width, height)
    animation_ticks = math.floor(FPS * ANIMATION['speed'])
    frame_ticks = math.ceil(FPS * ANIMATION['speed'] / ANIMATION['frames'])

    def __init__(self, x, y):
        super(WalkingTest, self).__init__(x, y)
        self.create(x, y, **OBJECT)

        # test
        self.position = PVector(400, -500)

        # left
        # self.position = PVector(0, 75)

        # right
        # self.position = PVector(900, 75)

        # top
        # self.position = PVector(200, 0)

        # bottom
        # self.position = PVector(200, 150)

    def apply_force(self, force):
        self.acceleration += force

    def update_forces(self, player, platforms):
        # fly_after(self, player)
        # run(self)
        # wind(self)
        gravity(self)
        # jump_from_platform(self, platforms)
        # push_from_platform(self, platforms)
        keep_on_platform(self, platforms)
        run_after(self, player)
        # fly_after(self, player)
        pass

    def update(self, player, platforms, map_position):
        # dead
        if self.hp <= 0:
            self.die()
            return

        # alive
        self.update_forces(player, platforms)
        self.move(map_position)
        self.fix_move(platforms, map_position)
