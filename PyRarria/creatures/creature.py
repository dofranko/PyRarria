import pygame as pg


class AbstractCreature(pg.sprite.Sprite):

    def __init__(self):
        super(AbstractCreature, self).__init__()

        # position
        self.x = None
        self.y = None
        self.w = None
        self.h = None
        self.v = None
        self.rect = pg.rect.Rect(0, 0, 0, 0)
        self.hpbar = None

        # counters
        self.jump_count = 0
        self.walk_count = 0
        self.bite_count = 0
        self.anim_count = 0

        # timers
        self.jump_timer = None
        self.walk_timer = None
        self.bite_timer = None
        self.anim_timer = None

        # flags
        self.is_left = False
        self.is_right = False
        self.is_stand = False
        self.is_enemy = False
        self.is_jump = False
        self.is_hpbar = False
        self.is_hitbox = True
        self.is_fixpos = False

        # specific for creature
        self.curr_hp = None
        self.max_hp = None
        self.items = []
        self.damage = None
        self.defense = None

        # generated in time
        self.steps = 0
        self.direction = 0

    def create(self, **attr):
        pass

    def draw(self, win):
        pass

    def hit(self, attack):
        pass

    def bite(self, enemy):
        pass

    def update(self, player):
        pass

    def move(self, player):
        pass

    def collision(self, player):
        pass

    def die(self):
        pass

