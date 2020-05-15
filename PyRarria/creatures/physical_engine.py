from PyRarria.creatures.global_settings import *
from PyRarria.creatures.vector import PVector
import random
import math

# forces
WIND = PVector(0.1, 0.1)
GRAVITY = PVector(0, 0.1)

# constants
MI = 0.05
RADIUS = 8
DISTANCE = 8
ANGLE_STEP = 0.5
EDGE_LIMIT = 50


def gravity(src):
    """Simple force of gravity.
    Q = m*g
    """
    grav = GRAVITY.copy()
    # grav *= src.mass
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
    pass


def run_away(src):
    pass


def run_after(src):
    pass


def jump(src):
    pass


def fly(src, target):
    # desired velocity
    desired = target.location - src.location
    desired.normalize()
    desired *= src.maxspeed

    # steering force
    steer = desired - src.velocity

    src.apply_force(steer)


def free_fly(src):
    # desired random
    src.angle += random.uniform(-ANGLE_STEP, ANGLE_STEP)
    rand = PVector(math.sin(src.angle), math.cos(src.angle))
    rand *= RADIUS

    # desired center
    if src.velocity.mag():
        desired = src.velocity.copy()
        desired.normalize()

    else:
        desired = PVector.random()

    desired *= DISTANCE
    desired += rand

    steer = desired - src.velocity
    src.apply_force(steer)


def fly_away(src, target):
    # desired velocity
    desired = target.location - src.location
    d = desired.mag()
    desired.normalize()

    if d < DISTANCE:
        m = (d*src.maxspeed) / DISTANCE
        desired *= m
    else:
        desired *= src.maxspeed

    # steering force
    steer = desired - src.velocity
    steer.limit(src.maxforce)
    src.apply_force(steer)


def fly_after(src):
    pass


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
