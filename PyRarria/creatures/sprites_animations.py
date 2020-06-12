import pygame as pg
from settings import *

load = pg.image.load

BIRD_LEFT = [
    load(CREATURES + "bird_01.png"),
    load(CREATURES + "bird_02.png"),
    load(CREATURES + "bird_03.png"),
    load(CREATURES + "bird_04.png"),
]

BIRD_RIGHT = [
    load(CREATURES + "bird_10.png"),
    load(CREATURES + "bird_11.png"),
    load(CREATURES + "bird_12.png"),
    load(CREATURES + "bird_13.png"),
]

COW_LEFT = [
    load(CREATURES + "cow_05.png"),
    load(CREATURES + "cow_06.png"),
    load(CREATURES + "cow_07.png"),
    load(CREATURES + "cow_08.png"),
]

COW_RIGHT = [
    load(CREATURES + "cow_13.png"),
    load(CREATURES + "cow_14.png"),
    load(CREATURES + "cow_15.png"),
    load(CREATURES + "cow_16.png"),
]

SHEEP_LEFT = [
    load(CREATURES + "sheep_05.png"),
    load(CREATURES + "sheep_06.png"),
    load(CREATURES + "sheep_07.png"),
    load(CREATURES + "sheep_08.png"),
]

SHEEP_RIGHT = [
    load(CREATURES + "sheep_13.png"),
    load(CREATURES + "sheep_14.png"),
    load(CREATURES + "sheep_15.png"),
    load(CREATURES + "sheep_16.png"),
]

ZOMBIE_LEFT = [
    load(CREATURES + "zombie_01.png"),
    load(CREATURES + "zombie_02.png"),
    load(CREATURES + "zombie_03.png"),
    load(CREATURES + "zombie_04.png"),
]

ZOMBIE_RIGHT = [
    load(CREATURES + "zombie_05.png"),
    load(CREATURES + "zombie_06.png"),
    load(CREATURES + "zombie_07.png"),
    load(CREATURES + "zombie_08.png"),
]

CHICKEN_LEFT = [
    load(CREATURES + "chicken_05.png"),
    load(CREATURES + "chicken_06.png"),
    load(CREATURES + "chicken_07.png"),
    load(CREATURES + "chicken_08.png"),
]

CHICKEN_RIGHT = [
    load(CREATURES + "chicken_13.png"),
    load(CREATURES + "chicken_14.png"),
    load(CREATURES + "chicken_15.png"),
    load(CREATURES + "chicken_16.png"),
]

BAT_LEFT = [
    load(CREATURES + "bat_06.png"),
    load(CREATURES + "bat_07.png"),
    load(CREATURES + "bat_08.png"),
    load(CREATURES + "bat_09.png"),
    load(CREATURES + "bat_10.png"),
]

BAT_RIGHT = [
    load(CREATURES + "bat_21.png"),
    load(CREATURES + "bat_22.png"),
    load(CREATURES + "bat_23.png"),
    load(CREATURES + "bat_24.png"),
    load(CREATURES + "bat_25.png"),
]

SKELETON_LEFT = [load(CREATURES + "skeleton_01.png"), load(CREATURES + "skeleton_02.png")]

SKELETON_RIGHT = [load(CREATURES + "skeleton_03.png"), load(CREATURES + "skeleton_04.png")]

SKELETONBOSS_LEFT = [load(CREATURES + "skeletonboss_01.png"), load(CREATURES + "skeletonboss_02.png")]

SKELETONBOSS_RIGHT = [load(CREATURES + "skeletonboss_03.png"), load(CREATURES + "skeletonboss_04.png")]

ARROW_LEFT = [load(CREATURES + "arrow_01.png")]
ARROW_RIGHT = [load(CREATURES + "arrow_02.png")]

WALKING_TEST_LEFT = [load(CREATURES + "walking_test_01.png")]
WALKING_TEST_RIGHT = [load(CREATURES + "walking_test_01.png")]


BIRD_ANIMATION = {
    "left": BIRD_LEFT,
    "right": BIRD_RIGHT,
    "frames": len(BIRD_LEFT),
    "width": BIRD_LEFT[0].get_rect().width,
    "height": BIRD_LEFT[0].get_rect().height,
    "speed": 0.5,  # animation duration in seconds
}

BAT_ANIMATION = {
    "left": BAT_LEFT,
    "right": BAT_RIGHT,
    "frames": len(BAT_LEFT),
    "width": BAT_LEFT[0].get_rect().width,
    "height": BAT_LEFT[0].get_rect().height,
    "speed": 0.75,  # animation duration in seconds
}

COW_ANIMATION = {
    "left": COW_LEFT,
    "right": COW_RIGHT,
    "frames": len(COW_LEFT),
    "width": COW_LEFT[0].get_rect().width,
    "height": COW_LEFT[0].get_rect().height,
    "speed": 0.5,
}

SHEEP_ANIMATION = {
    "left": SHEEP_LEFT,
    "right": SHEEP_RIGHT,
    "frames": len(SHEEP_LEFT),
    "width": SHEEP_LEFT[0].get_rect().width,
    "height": SHEEP_LEFT[0].get_rect().height,
    "speed": 0.5,
}

SKELETON_ANIMATION = {
    "left": SKELETON_LEFT,
    "right": SKELETON_RIGHT,
    "frames": len(SKELETON_LEFT),
    "width": SKELETON_LEFT[0].get_rect().width,
    "height": SKELETON_LEFT[0].get_rect().height,
    "speed": 0.5,
}

SKELETONBOSS_ANIMATION = {
    "left": SKELETONBOSS_LEFT,
    "right": SKELETONBOSS_RIGHT,
    "frames": len(SKELETONBOSS_LEFT),
    "width": SKELETONBOSS_LEFT[0].get_rect().width,
    "height": SKELETONBOSS_LEFT[0].get_rect().height,
    "speed": 0.5,
}

ZOMBIE_ANIMATION = {
    "left": ZOMBIE_LEFT,
    "right": ZOMBIE_RIGHT,
    "frames": len(ZOMBIE_LEFT),
    "width": ZOMBIE_LEFT[0].get_rect().width,
    "height": ZOMBIE_LEFT[0].get_rect().height,
    "speed": 1.0,
}

ARROW_ANIMATION = {
    "left": ARROW_LEFT,
    "right": ARROW_RIGHT,
    "frames": len(ARROW_LEFT),
    "width": ARROW_LEFT[0].get_rect().width,
    "height": ARROW_LEFT[0].get_rect().height,
    "speed": 2,
}

CHICKEN_ANIMATION = {
    "left": CHICKEN_LEFT,
    "right": CHICKEN_RIGHT,
    "frames": len(CHICKEN_LEFT),
    "width": CHICKEN_LEFT[0].get_rect().width,
    "height": CHICKEN_LEFT[0].get_rect().height,
    "speed": 1,
}

WALKING_TEST_ANIMATION = {
    "left": WALKING_TEST_LEFT,
    "right": WALKING_TEST_RIGHT,
    "frames": len(WALKING_TEST_LEFT),
    "width": WALKING_TEST_LEFT[0].get_rect().width,
    "height": WALKING_TEST_LEFT[0].get_rect().height,
    "speed": 1,
}
