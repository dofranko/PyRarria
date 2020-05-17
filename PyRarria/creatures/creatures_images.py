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


DOG_LEFT = [
    load('img/dogL01.png'), load('img/dogL02.png'),
    load('img/dogL03.png'), load('img/dogL04.png'),
    load('img/dogL05.png'), load('img/dogL06.png'),
    load('img/dogL07.png'), load('img/dogL08.png'),
    load('img/dogL09.png'), load('img/dogL10.png')]

DOG_RIGHT = [
    load('img/dogR01.png'), load('img/dogR02.png'),
    load('img/dogR03.png'), load('img/dogR04.png'),
    load('img/dogR05.png'), load('img/dogR06.png'),
    load('img/dogR07.png'), load('img/dogR08.png'),
    load('img/dogR09.png'), load('img/dogR10.png')]

DOG_FRAMES = 10


BIRD_ANIMATION = {
    'left': BIRD_LEFT,
    'right': BIRD_RIGHT,
    'frames': len(BIRD_LEFT),
    'width': BIRD_LEFT[0].get_rect().width,
    'height': BIRD_LEFT[0].get_rect().height,
    'speed': 0.5,  # animation duration in seconds
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
