from creatures.physical_engine import *
from creatures.sprites_attributes import SKELETONBOSS
from creatures.sprites_animations import SKELETONBOSS_ANIMATION
from creatures.sprites_tree.arrow import Arrow
from creatures.sprites_tree.walking_sprite import WalkingSprite
from creatures.sprites_tree.skeleton import Skeleton
from settings import FPS

import math


ANIMATION = SKELETONBOSS_ANIMATION
OBJECT = SKELETONBOSS


class SkeletonBoss(Skeleton):

    # static variables
    animation = [ANIMATION["left"], ANIMATION["right"]]
    frames = ANIMATION["frames"]
    width = ANIMATION["width"]
    height = ANIMATION["height"]
    radius = min(width, height)
    animation_ticks = math.floor(FPS * ANIMATION["speed"])
    frame_ticks = math.ceil(FPS * ANIMATION["speed"] / ANIMATION["frames"])

    def __init__(self, x, y):
        super(SkeletonBoss, self).__init__(x, y)
        self.create(x, y, **OBJECT)

    def shoot(self, player, arrows):
        if self.shot_count > 0:
            self.shot_count -= 1
        else:
            arrow = Arrow(self.position.x, self.position.y)
            bullet(arrow, self.position, player.position)

            arrows.add(arrow)
            self.shot_count = 10
