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
        self.hbox = []

        # counters
        self.jump_count = None
        self.walk_count = None
        self.hit_count = None
        self.anime_count = 0

        # boolean
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

    def draw(self, win):
        pass

    def hit(self, attack):
        pass

    def bite(self, enemy):
        pass

    def move(self, player):
        pass

