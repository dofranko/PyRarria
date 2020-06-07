import pygame as pg
from creatures.vector import PVector


class AbstractSprite(pg.sprite.Sprite):

    # static variables
    animation = None
    frames = None
    width = None
    height = None
    radius = None
    animation_ticks = None
    frame_ticks = None

    def __init__(self, x, y):
        super(AbstractSprite, self).__init__()

        # variables
        self.radius = None
        self.angle = None
        self.mass = None

        # limits
        self.maxspeed = None
        self.maxforce = None
        self.maxhp = None
        self.manoeuvrability = None

        # flags
        self.is_enemy = False
        self.is_hpbar = False
        self.is_hitbox = True
        self.is_fixpos = False
        self.is_target = False

        # counters
        self.anim_count = None
        self.bite_count = None
        self.shot_count = None
        self.freeze_count = None

        # vectors
        self.position = PVector(x, y)
        self.velocity = PVector(0, 0)
        self.acceleration = PVector(0, 0)
        self.acceleration_no_limit = PVector(0, 0)

        # body, hitbox
        self.rect = None
        self.body = None
        self.hpbar = None

        # sprite specific
        self.hp = None
        self.items = []
        self.damage = None
        self.defense = None

    def create(self, **attr):
        pass

    def draw(self, win):
        pass

    def hit(self, damage_value):
        pass

    def bite(self, player):
        pass

    def shoot(self, player, arrows):
        pass

    def update(self, player, platforms, map_position, items_factory):
        pass

    def update_forces(self, player, platforms):
        pass

    def apply_force(self, force):
        pass

    def apply_force_no_limit(self, force):
        pass

    def move(self, map_position):
        pass

    def fix_move(self, platforms, map_position):
        pass

    def die(self, items_factory):
        pass
