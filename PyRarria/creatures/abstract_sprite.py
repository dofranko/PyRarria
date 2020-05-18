import pygame as pg

from PyRarria.creatures.vector import PVector


class AbstractSprite(pg.sprite.Sprite):

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

        # counters
        self.anim_count = None
        self.bite_count = None
        self.shot_count = None

        # vectors
        self.location = PVector(x, y)
        self.velocity = PVector(0, 0)
        self.acceleration = PVector(0, 0)

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

    def hit(self, weapon):
        pass

    def bite(self, player):
        pass

    def update(self, player, platforms):
        pass

    def update_forces(self, player, platforms):
        pass

    def apply_force(self, player):
        pass

    def move(self, player):
        pass

    def map_move(self, dx, dy):
        pass

    def die(self):
        pass
