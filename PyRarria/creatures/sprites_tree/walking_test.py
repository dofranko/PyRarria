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

        # TEST dodac position
        self.position = PVector(400, 58)

    def apply_force(self, force):
        self.acceleration += force

    def update_forces(self, player, platforms):
        # fly_after(self, player)
        # run(self)
        # gravity(self)
        # jump_from_platform2(self, platforms)
        # push_from_platform(self, platforms)
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

    def move(self, map_position):
        # move
        self.velocity += self.acceleration
        self.velocity.xlimit(self.maxspeed)
        self.position += self.velocity
        self.acceleration.zero()

        # update body
        self.body.topleft = (self.position + map_position).repr()
        self.rect.topleft = (self.position + map_position).repr()
        self.hpbar.center(self.body.midtop)

        # update animation counter
        self.anim_count -= 1
        self.anim_count %= self.animation_ticks
