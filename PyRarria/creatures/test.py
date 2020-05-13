import pygame as pg
from pygame.sprite import Group
from PyRarria.creatures.global_settings import *
from pygame.sprite import spritecollide
from PyRarria.creatures.dog import Dog
from PyRarria.creatures.player_test import Player
from PyRarria.weapon import Weapon

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_a,
    K_w,
    K_s,
    K_d,
    QUIT,
    MOUSEMOTION,
)

pg.init()



# images / fonts
bg = pg.image.load('images/bg.jpg')
char = pg.image.load('images/standing.png')
font = pg.font.SysFont('comicsans', 30, True, False)

# window / clock
win = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()

# groups
all_sprites = Group()
creatures = Group()

# objects
man = Player(300, 300, 64, 64)
dog = Dog(300, 325)
weapon = Weapon(200, 200, 20, 20)

# sprites
creatures.add(dog)
all_sprites.add(dog)
all_sprites.add(man)


score = 0


def update_engine():
    # hit creatures
    for creature in creatures:
        creature.hit(weapon)

    # update creatures
    for creature in creatures:
        creature.update(man)


def redraw_engine():
    # background
    win.blit(bg, (0, 0))

    # player
    man.draw(win)

    # weapon
    weapon.draw(win)

    # creatures
    for creature in creatures:
        creature.draw(win)

    # update
    pg.display.update()


def redraw_window():
    update_engine()
    redraw_engine()


run = True
while run:
    # clock
    clock.tick(FPS)

    # events
    for event in pg.event.get():
        if event.type == QUIT:
            run = False

        elif event.type == MOUSEMOTION:
            weapon.move(event.pos)

    # keyboard
    keys = pg.key.get_pressed()
    man.standing = True

    if keys[K_ESCAPE]:
        run = False

    if keys[K_LEFT] or keys[K_a]:
        man.x -= man.v
        man.left = True
        man.right = False
        man.standing = False

    if keys[K_RIGHT] or keys[K_d]:
        man.x += man.v
        man.right = True
        man.left = False
        man.standing = False

    if keys[K_UP] or keys[K_w]:
        man.y -= man.v
        man.standing = False

    if keys[K_DOWN] or keys[K_s]:
        man.y += man.v
        man.standing = False

    # repair
    if man.x < 0:
        man.x = 0

    elif man.x > SCREEN_WIDTH - man.width:
        man.x = SCREEN_WIDTH - man.width

    if man.y < 0:
        man.y = 0

    elif man.y > SCREEN_HEIGHT - man.height:
        man.y = SCREEN_HEIGHT - man.height

    update_engine()
    redraw_engine()

pg.quit()
