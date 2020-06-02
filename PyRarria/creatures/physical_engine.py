from PyRarria.creatures.test_global_settings import *
from PyRarria.creatures.vector import PVector
import pygame as pg
import random
import math

# forces
WIND = PVector(0.000001, 0.0)
GRAVITY = PVector(0, 2.0)
# GRAVITY = PVector(0, 0.1)
# REACTION = PVector(0, -0.1)
REACTION = PVector(0,-3)

# constants
MI = 0.05
EDGE_LIMIT = 50
ARC_LENGTH = 2 * math.pi
ARC_STEP = ARC_LENGTH / 15
MOVE_LENGTH = 10
MOVE_STEP = MOVE_LENGTH / 15


def gravity(src):
    """Simple force of gravity.
    Q = m*g
    """
    grav = GRAVITY.copy()
    src.apply_force(grav)


def reaction(src):
    """Reaction force.
    R = Q
    """
    reac = REACTION.copy()
    src.apply_force(reac)
    src.velocity.y = 0


def wind(src):
    """Applies wind force.
    F = const.
    """
    src.apply_force(WIND)


def friction(src):
    """Applies friction force.
    F = -1 * MI * N * v^
    """
    force = src.velocity.copy()
    force *= -1
    force.normalize()
    force *= MI
    force /= src.mass
    src.apply_force(force)


def run(src):
    """Random running according to maxspeed and manoeuvrability."""

    # desired velocity
    desired = src.velocity.copy()
    step = src.maxspeed * src.manoeuvrability
    desired.x += random.uniform(-step, step)
    desired.xflat()

    # steering force
    steer = desired - src.velocity
    src.apply_force(steer)


def run_away(src, target):
    """Runs away from the target on horizontal line, stops close to it.
    A greater distance in less force."""

    # desired velocity
    desired = target.location - src.location
    desired.xflat()
    desired *= -1
    d = desired.mag()
    desired.normalize()
    if d:
        desired *= src.maxspeed * 150 / d
    else:
        desired *= src.maxspeed * 150 / 1000

    # steering force
    steer = desired - src.velocity
    src.apply_force(steer)


def run_after(src, target):
    """Runs to the target only on horizontal line."""

    # desired velocity
    desired = target.location - src.location
    desired.xflat()
    d = desired.mag()
    desired.normalize()

    if d < src.radius:
        m = (d*src.maxspeed) / src.radius
        desired *= m
    else:
        desired *= src.maxspeed

    # steering force
    steer = desired - src.velocity
    src.apply_force(steer)


def jump(src):
    """Performs single jump"""
    jmp = PVector(src.velocity.xdirection(), -src.maxforce/4)
    src.apply_force(jmp)


def bullet(src, src_location, dest_location):
    """Calculates and applies force to reach dest from src."""

    # TODO zero division error

    # TEST
    x0 = src_location.x
    y0 = src_location.y

    x1 = dest_location.x
    y1 = dest_location.y

    dx = x1 - x0
    dy = y1 - y0
    sx = x0 + x1

    g = 0.1
    vx = dx/100

    if dx == 0:
        return
    vy = vx * abs(dy/dx) + 0.5 * g * abs(dx/vx)

    # STATS
    # print('x0 = ', x0)
    # print('y0 = ', y0)
    # print('x1 = ', x1)
    # print('y1 = ', y1)
    #
    # print('sx = ', sx)
    # print('dx = ', dx)
    # print('dy = ', dy)
    #
    # print('vx = ', vx)
    # print('vy = ', vy)

    # TEMP
    # a = dy/dx + 0.1*sx
    # b = src_location.y + 0.1*(src_location.x**2) - a*src_location.x
    # print('a = ', a)
    # print('b = ', b)
    # print('real y = ', src_location.y)
    # print('test y = ', -0.1*src_location.x**2 + a*src_location.x + b)

    # p = dy/dx + 0.5 * g * sx
    # q = y0 + x0 * (0.5*g*x0 - p)

    # a = -g*x0 + p
    # alpha = 180 * math.atan(a) / math.pi

    # a = (y0*dx + x0*dy) / (x0*x1*dx)
    # b = dy/dx + a*sx

    # a = dy/dx + 0.5*g*sx
    # alpha = -g*x0 + a
    # s = math.sqrt(0.1 * (dx**2) / (dx - dy))
    # s *= 0.7

    force = PVector(vx, -vy)
    src.apply_force(force)


def track(src, target):
    """Source tracks the target, stops close to it."""

    # desired velocity
    desired = target.location - src.location
    desired.normalize()
    desired *= src.maxspeed

    # steering force
    steer = desired - src.velocity
    steer /= src.mass
    src.apply_force(steer)


def fly(src):
    """Random flying according to maxspeed and manoeuvrability."""

    # desired direction
    src.angle += random.uniform(-ARC_STEP, ARC_STEP)
    src.angle = math.fmod(src.angle, ARC_LENGTH)

    rand = PVector(math.sin(src.angle), math.cos(src.angle))
    rand *= src.maxspeed * src.manoeuvrability

    # desired length
    if src.velocity.mag():
        desired = src.velocity.copy()
        desired.normalize()
    else:
        desired = PVector.random()

    desired *= src.maxspeed
    desired += rand

    # steering force
    steer = desired - src.velocity
    src.apply_force(steer)


def fly_after(src, target):
    """Flies straight to the target, stops close to it."""

    # desired velocity
    desired = target.location - src.location
    d = desired.mag()
    desired.normalize()

    if d < src.radius:
        m = (d*src.maxspeed) / src.radius
        desired *= m
    else:
        desired *= src.maxspeed

    # steering force
    steer = desired - src.velocity
    src.apply_force(steer)


def fly_away(src, target):
    """Flies away from the target, stops close to it.
    A greater distance in less force."""

    # desired velocity
    desired = target.location - src.location
    desired *= -1
    d = desired.mag()
    desired.normalize()
    desired *= src.maxspeed * 150 / d

    # steering force
    steer = desired - src.velocity
    src.apply_force(steer)


def edges(src):
    """Checks if the object does not go beyond the screen.
    If true, object turns back with the opposite direction and max velocity."""

    # horizontal
    if src.location.x < EDGE_LIMIT:
        desired = PVector(src.maxspeed, src.velocity.y)
        steer = desired - src.velocity
        src.apply_force(steer)
    elif src.location.x > SCREEN_WIDTH - EDGE_LIMIT:
        desired = PVector(-src.maxspeed, src.velocity.y)
        steer = desired - src.velocity
        src.apply_force(steer)

    # vertical
    if src.location.y < EDGE_LIMIT:
        desired = PVector(src.velocity.x, src.maxspeed)
        steer = desired - src.velocity
        src.apply_force(steer)
    elif src.location.y > SCREEN_HEIGHT - EDGE_LIMIT:
        desired = PVector(src.velocity.x, -src.maxspeed)
        steer = desired - src.velocity
        src.apply_force(steer)


def edges_stop(src):
    """Checks if the object does not go beyond the screen.
    Ball stops whet touches the edge."""

    # horizontal
    if src.location.x < 0:
        src.velocity.x = 0
        src.location.x = 0
    elif src.location.x > SCREEN_WIDTH:
        src.velocity.x = 0
        src.location.x = SCREEN_WIDTH

    # vertical
    if src.location.y < 0:
        src.velocity.y = 0
        src.location.y = 0
    elif src.location.y > SCREEN_HEIGHT:
        src.velocity.y = 0
        src.location.y = SCREEN_HEIGHT


def edges_delete(src):
    """Deletes object if it goes off the screen."""

    if src.location.x < 0 or src.location.x > SCREEN_WIDTH:
        src.die()

    elif src.location.y > SCREEN_HEIGHT:
        src.die()

    
def edges_ball(src):
    """Checks if the object goes off the screen.
    Bounces off the edge like a ball."""

    # horizontal
    if src.location.x < 0:
        src.velocity.x *= -1
        src.location.x = 0
    elif src.location.x > SCREEN_WIDTH:
        src.velocity.x *= -1
        src.location.x = SCREEN_WIDTH

    # vertical
    if src.location.y < 0:
        src.velocity.y *= -1
        src.location.y = 0
    elif src.location.y > SCREEN_HEIGHT:
        src.velocity.y *= -1
        src.location.y = SCREEN_HEIGHT


def init_move(src):
    """Initializes velocity if creature isn't moving."""

    if src.velocity.y == 0 and src.velocity.x == 0:
        force = PVector(-src.maxspeed, 0)
        src.apply_force(force)


def keep_on_platform(src, platforms):
    """Inverts speed vector if creature reaches platform edge."""

    hits = pg.sprite.spritecollide(src, platforms, False)
    if hits:
        reaction(src)
        right = hits[0].rect.right
        left = hits[0].rect.left

        if src.location.x > right:
            src.velocity.x *= -1
            src.location.x = right

        elif src.location.x < left:
            src.velocity.x *= -1
            src.location.x = left


def push_from_platform(src, platforms):
    """Adds extra force if creature reaches platform edge to push it out."""

    hits = pg.sprite.spritecollide(src, platforms, False)
    if hits:
        reaction(src)
        right = hits[0].rect.right
        left = hits[0].rect.left

        if src.location.x > right:
            src.apply_force(PVector(src.maxforce, 0))

        elif src.location.x < left:
            src.apply_force(PVector(-src.maxforce, 0))


def jump_from_platform(src, platforms):
    """If creature is on edge, jumps forward."""

    hits = pg.sprite.spritecollide(src, platforms, False)
    if hits:
        reaction(src)
        right = hits[0].rect.right
        left = hits[0].rect.left

        if src.location.x > right:
            jump(src)

        elif src.location.x < left:
            jump(src)
