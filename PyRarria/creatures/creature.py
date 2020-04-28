class Creature(object):

    left = []
    right = []

    def __init__(self, x, y):

        # position
        self.x = None
        self.y = None
        self.w = None
        self.h = None
        self.v = None
        self.hbox = (0, 0, 0, 0)

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
        self.is_enemy = False
        self.is_jump = False
        self.is_hpbar = False

        # specific for creature
        self.hp = None
        self.items = []
        self.attack = None
        self.defense = None

        # generated in time
        self.steps = 0
        self.direction = 0

    def create(self, **attr):
        pass

    def draw(self, win, player):
        pass

    def hit(self, attack):
        pass

    def bite(self, enemy):
        pass

    def move(self, player):
        pass

    def collision(self, player):
        pass

    def die(self):
        pass

