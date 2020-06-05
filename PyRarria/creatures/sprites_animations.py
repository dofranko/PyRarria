import pygame as pg

load = pg.image.load


BIRD_LEFT = [
    load('img/bird_01.png'), load('img/bird_02.png'),
    load('img/bird_03.png'), load('img/bird_04.png')]

BIRD_RIGHT = [
    load('img/bird_10.png'), load('img/bird_11.png'),
    load('img/bird_12.png'), load('img/bird_13.png')]

COW_LEFT = [
    load('img/cow_05.png'), load('img/cow_06.png'),
    load('img/cow_07.png'), load('img/cow_08.png')]

COW_RIGHT = [
    load('img/cow_13.png'), load('img/cow_14.png'),
    load('img/cow_15.png'), load('img/cow_16.png')]

SHEEP_LEFT = [
    load('img/sheep_05.png'), load('img/sheep_06.png'),
    load('img/sheep_07.png'), load('img/sheep_08.png')]

SHEEP_RIGHT = [
    load('img/sheep_13.png'), load('img/sheep_14.png'),
    load('img/sheep_15.png'), load('img/sheep_16.png')]

ZOMBIE_LEFT = [
    load('img/zombie_01.png'), load('img/zombie_02.png'),
    load('img/zombie_03.png'), load('img/zombie_04.png')]

ZOMBIE_RIGHT = [
    load('img/zombie_05.png'), load('img/zombie_06.png'),
    load('img/zombie_07.png'), load('img/zombie_08.png')]

CHICKEN_LEFT = [
    load('img/chicken_05.png'), load('img/chicken_06.png'),
    load('img/chicken_07.png'), load('img/chicken_08.png')]

CHICKEN_RIGHT = [
    load('img/chicken_13.png'), load('img/chicken_14.png'),
    load('img/chicken_15.png'), load('img/chicken_16.png')]

BAT_LEFT = [
    load('img/bat_06.png'), load('img/bat_07.png'),
    load('img/bat_08.png'), load('img/bat_09.png'),
    load('img/bat_10.png')]

BAT_RIGHT = [
    load('img/bat_21.png'), load('img/bat_22.png'),
    load('img/bat_23.png'), load('img/bat_24.png'),
    load('img/bat_25.png')]

SKELETON_LEFT = [load('img/skeleton_01.png'), load('img/skeleton_02.png')]
SKELETON_RIGHT = [load('img/skeleton_03.png'), load('img/skeleton_04.png')]

ARROW_LEFT = [load('img/arrow_01.png')]
ARROW_RIGHT = [load('img/arrow_02.png')]

WALKING_TEST_LEFT = [load('img/walking_test_01.png')]
WALKING_TEST_RIGHT = [load('img/walking_test_01.png')]


BIRD_ANIMATION = {
    'left': BIRD_LEFT,
    'right': BIRD_RIGHT,
    'frames': len(BIRD_LEFT),
    'width': BIRD_LEFT[0].get_rect().width,
    'height': BIRD_LEFT[0].get_rect().height,
    'speed': 0.5,  # animation duration in seconds
}

BAT_ANIMATION = {
    'left': BAT_LEFT,
    'right': BAT_RIGHT,
    'frames': len(BAT_LEFT),
    'width': BAT_LEFT[0].get_rect().width,
    'height': BAT_LEFT[0].get_rect().height,
    'speed': 0.75,  # animation duration in seconds
}

COW_ANIMATION = {
    'left': COW_LEFT,
    'right': COW_RIGHT,
    'frames': len(COW_LEFT),
    'width': COW_LEFT[0].get_rect().width,
    'height': COW_LEFT[0].get_rect().height,
    'speed': 0.5,
}

SHEEP_ANIMATION = {
    'left': SHEEP_LEFT,
    'right': SHEEP_RIGHT,
    'frames': len(SHEEP_LEFT),
    'width': SHEEP_LEFT[0].get_rect().width,
    'height': SHEEP_LEFT[0].get_rect().height,
    'speed': 0.5,
}

SKELETON_ANIMATION = {
    'left': SKELETON_LEFT,
    'right': SKELETON_RIGHT,
    'frames': len(SKELETON_LEFT),
    'width': SKELETON_LEFT[0].get_rect().width,
    'height': SKELETON_LEFT[0].get_rect().height,
    'speed': 0.5,
}

ZOMBIE_ANIMATION = {
    'left': ZOMBIE_LEFT,
    'right': ZOMBIE_RIGHT,
    'frames': len(ZOMBIE_LEFT),
    'width': ZOMBIE_LEFT[0].get_rect().width,
    'height': ZOMBIE_LEFT[0].get_rect().height,
    'speed': 1.0,
}

ARROW_ANIMATION = {
    'left': ARROW_LEFT,
    'right': ARROW_RIGHT,
    'frames': len(ARROW_LEFT),
    'width': ARROW_LEFT[0].get_rect().width,
    'height': ARROW_LEFT[0].get_rect().height,
    'speed': 2,
}

CHICKEN_ANIMATION = {
    'left': CHICKEN_LEFT,
    'right': CHICKEN_RIGHT,
    'frames': len(CHICKEN_LEFT),
    'width': CHICKEN_LEFT[0].get_rect().width,
    'height': CHICKEN_LEFT[0].get_rect().height,
    'speed': 2,
}

WALKING_TEST_ANIMATION = {
    'left': WALKING_TEST_LEFT,
    'right': WALKING_TEST_RIGHT,
    'frames': len(WALKING_TEST_LEFT),
    'width': WALKING_TEST_LEFT[0].get_rect().width,
    'height': WALKING_TEST_LEFT[0].get_rect().height,
    'speed': 1,
}