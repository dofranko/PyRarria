from PyRarria.creatures.global_settings import *
from PyRarria.creatures.vector import PVector
import random
import math

# forces
WIND = PVector(0.1, 0.1)
GRAVITY = PVector(0, 0.1)

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
    pass


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

    
def edges_ball(src):
    """Checks if the object does not go beyond the screen.
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
