from settings import *
from creatures.vector import PVector
import pygame as pg
import random
import math

# forces
WIND = PVector(-0.05, 0.0)
GRAVITY = PVector(0, 0.2)
GRAVITY_BULLET = PVector(0, 0.1)
REACTION = PVector(0, -0.1)

# constants
MI = 0.05
EDGE_LIMIT = -200
ARC_LENGTH = 2 * math.pi
ARC_STEP = ARC_LENGTH / 15
MOVE_LENGTH = 10
MOVE_STEP = MOVE_LENGTH / 15
MAX_XPUSH = 50
MAX_YPUSH = 15


def gravity(src):
    """Simple force of gravity.
    Q = m*g
    """
    grav = GRAVITY.copy()
    src.apply_force(grav)


def gravity_bullet(src):
    """Simple force of gravity. Only for flying objects.
    Q = m*g
    """
    grav = GRAVITY_BULLET.copy()
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
    steer.xflat()
    src.apply_force(steer)


def run_away(src, target):
    """Runs away from the target on horizontal line, stops close to it.
    A greater distance in less force."""

    # desired velocity
    desired = target.position - src.position
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
    steer.xflat()
    src.apply_force(steer)


def run_after(src, target):
    """Runs to the target only on horizontal line."""
    if src.velocity.y != 0.0:
        return

    # desired velocity
    desired = target.position - src.position
    desired.xflat()
    d = desired.mag()
    desired.normalize()

    if d < src.radius:
        m = (d * src.maxspeed) / src.radius
        desired *= m
    else:
        desired *= src.maxspeed

    # steering force
    steer = desired - src.velocity
    steer.xflat()
    src.apply_force(steer)


def jump(src):
    """Performs single jump"""
    jmp = PVector(src.velocity.xdirection() * src.maxspeed, -src.maxspeed / 8)
    src.apply_force(jmp)


def stop(src):
    """Stops creature if it doesn't fall."""
    if src.velocity.y == 0.0:
        src.velocity.x = 0.0


def freeze(src):
    """Reduces creature acceleration."""
    if src.freeze_count > 0:
        src.freeze_count -= 1
        src.acceleration.limit(0.01)
        src.acceleration_no_limit.limit(0.01)
        src.velocity.limit(0.5)


def push_away(src, player, damage):
    """Pushes the opponent of the player."""
    delta = src.position - player.position
    direction = delta.xdirection()

    force = PVector(direction * damage * MAX_XPUSH, -damage * MAX_YPUSH)
    src.apply_force_no_limit(force)


def bullet(src, src_location, dest_location):
    """Calculates and applies force to reach dest from src."""
    x0 = src_location.x
    y0 = src_location.y

    x1 = dest_location.x
    y1 = dest_location.y

    dx = x1 - x0
    dy = y1 - y0

    vx = dx / 100
    if dx == 0:
        return
    vy = vx * abs(dy / dx) + 0.5 * GRAVITY_BULLET.y * abs(dx / vx)

    force = PVector(vx, -vy)
    src.apply_force(force)


def track(src, target):
    """Source tracks the target, stops close to it."""

    # desired velocity
    desired = target.position - src.position
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
    desired = target.position - src.position
    d = desired.mag()
    desired.normalize()

    if d < src.radius:
        m = (d * src.maxspeed) / src.radius
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
    desired = target.position - src.position
    desired *= -1
    d = desired.mag()
    desired.normalize()
    desired *= src.maxspeed * 150 / d

    # steering force
    steer = desired - src.velocity
    src.apply_force(steer)


def edges_bounce(src):
    """Checks if the object does not go beyond the screen.
    If true, object turns back with the opposite direction and max velocity."""

    # horizontal
    if src.rect.left < EDGE_LIMIT:
        desired = PVector(src.maxspeed, src.velocity.y)
        steer = desired - src.velocity
        src.apply_force(steer)
    elif src.rect.right > WIDTH - EDGE_LIMIT:
        desired = PVector(-src.maxspeed, src.velocity.y)
        steer = desired - src.velocity
        src.apply_force(steer)

    # vertical
    if src.rect.top < EDGE_LIMIT:
        desired = PVector(src.velocity.x, src.maxspeed)
        steer = desired - src.velocity
        src.apply_force(steer)
    elif src.rect.bottom > HEIGHT - EDGE_LIMIT:
        desired = PVector(src.velocity.x, -src.maxspeed)
        steer = desired - src.velocity
        src.apply_force(steer)


def edges_delete(src):
    """Deletes object if it goes off the screen."""

    if src.rect.right < 0 or src.rect.left > WIDTH:
        src.hp = -1.0

    elif src.rect.top > HEIGHT:
        src.hp = -1.0


def map_delete(src):
    """Deletes object if it flies out of the map."""
    pass


def init_move(src):
    """Initializes velocity if creature isn't moving."""

    if src.velocity.y == 0 and src.velocity.x == 0:
        force = PVector(-src.maxspeed, 0)
        src.apply_force(force)


def keep_on_platform(src, blocks):
    """Inverts speed vector if creature reaches platform edge."""

    hits = pg.sprite.spritecollide(src, blocks, False)
    if hits:

        # reaction(src)

        if src.rect.centerx > hits[0].rect.right:
            desired = PVector(-1, src.velocity.y)
            steer = desired - src.velocity
            src.apply_force(steer)

        elif src.rect.centerx < hits[0].rect.left:
            desired = PVector(1, src.velocity.y)
            steer = desired - src.velocity
            src.apply_force(steer)


def push_from_platform(src, blocks):
    """Inverts speed vector if creature reaches platform edge."""

    hits = pg.sprite.spritecollide(src, blocks, False)
    if hits:

        # reaction(src)

        if src.rect.centerx > hits[0].rect.right:
            desired = PVector(2, src.velocity.y)
            steer = desired - src.velocity
            src.apply_force(steer)

        elif src.rect.centerx < hits[0].rect.left:
            desired = PVector(-2, src.velocity.y)
            steer = desired - src.velocity
            src.apply_force(steer)


def jump_from_platform(src, blocks):
    """If creature is on edge, jumps forward."""

    hits = pg.sprite.spritecollide(src, blocks, False)
    if hits:

        # reaction(src)

        if src.rect.centerx > hits[0].rect.right:
            jump(src)

        elif src.rect.centerx < hits[0].rect.left:
            jump(src)


def bounce_from_platform(src, blocks):
    """If creature collides with blocks, moves in opposite direction."""
    hits = pg.sprite.spritecollide(src, blocks, False)
    if hits:
        print("hits")
        if src.rect.left < hits[0].rect.left:
            src.apply_force(PVector(-src.maxforce, 0))

        elif src.rect.right > hits[0].rect.right:
            src.apply_force(PVector(src.maxforce, 0))

        if src.rect.top < hits[0].rect.top:
            src.apply_force(PVector(0, -src.maxforce))

        elif src.rect.bottom > hits[0].rect.bottom:
            src.apply_force(PVector(0, +src.maxforce))


def platform_stop(src, blocks):
    """If creature collides with blocks, stopes."""
    hits = pg.sprite.spritecollide(src, blocks, False)
    if hits:
        reaction(src)
        src.velocity.x = 0
        return True

    return False
