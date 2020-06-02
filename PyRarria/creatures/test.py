import pygame as pg
from pygame.sprite import Group

from PyRarria.creatures.creatures_engine import CreaturesEngine
from PyRarria.creatures.sprites_tree.arrow import Arrow
from PyRarria.creatures.sprites_tree.bird import Bird
from PyRarria.creatures.sprites_tree.skeleton import Skeleton
from PyRarria.creatures.test_global_settings import *
from PyRarria.creatures.test_player import Player
from PyRarria.creatures.teat_weapon import Weapon

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

# pygame init
pg.init()

# test constants
BACKGORUND = pg.image.load('images/bg.jpg')
CHAR = pg.image.load('images/standing.png')
FONT = pg.font.SysFont('comicsans', 30, True, False)

# window / clock
win = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()

# groups
all_sprites = Group()
all_creatures = Group()
creatures = Group()
archers = Group()
arrows = Group()
platforms = Group()

# sprites
man = Player(400, 300, 64, 64)
weapon = Weapon(200, 200, 20, 20)
bird = Bird(50, 300)
skeleton = Skeleton(200, 200)
arrow = Arrow(50, 50)
# platform = Platform(100, SCREEN_HEIGHT/2, SCREEN_WIDTH - 200, 30)

# groups init
all_sprites.add(man)

# all_sprites.add(bird)
# creatures.add(bird)

# all_sprites.add(skeleton)
# creatures.add(skeleton)
# archers.add(skeleton)

# all_sprites.add(arrow)
# arrows.add(arrow)

# all_sprites.add(platform)
# platforms.add(platform)

# creatures engine
creatures_engine = CreaturesEngine(win, platforms, man,
                                   all_creatures, archers, arrows)

def update_engine():
    # # hit
    # for creature in creatures:
    #     creature.hit(weapon)

    # # bite
    # for creature in creatures:
    #     creature.bite(man)

    # # shot
    # for archer in archers:
    #     archer.shoot(man, arrows)

    # # update creatures
    # for creature in creatures:
    #     creature.update(man, platforms)
    #
    # # update arrows
    # for arr in arrows:
    #     arr.update(man, platforms)
    creatures_engine.update()


def redraw_engine():
    # background
    win.blit(BACKGORUND, (0, 0))

    # platforms
    for plat in platforms:
        plat.draw(win)

    # player
    man.draw(win)

    # weapon
    weapon.draw(win)

    # # creatures
    # for creature in creatures:
    #     creature.draw(win)
    #
    # # arrows
    # for arr in arrows:
    #     arr.draw(win)
    creatures_engine.draw()

    # update
    pg.display.update()


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

    man.location.x = man.x
    man.location.y = man.y
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
