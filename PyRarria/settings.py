# game options/settings
TITLE = "PyRarria"
WIDTH = 800
HEIGHT = 600
FPS = 60

# Player properties
PLAYER_MOVE = {
    'PLAYER_ACC': 5
}
PLAYER_FRICTION = -0.2
PLAYER_GRAV = 0.8
MAX_VEL_Y = 15

# Health/Mana bar properties
HEART_VALUE = 195
STAR_VALUE = 195
HEALTH_RECOVERY_VALUE = 1
MANA_RECOVERY_VALUE = 1
MAX_HEALTH = 20 * HEART_VALUE
MIN_HEALTH = 5 * HEART_VALUE
MAX_MANA = 20 * STAR_VALUE
MIN_MANA = 5 * STAR_VALUE

SPELL_DELAYS = {
    'fireball': 400,
    'smallfire': 5000,
    'frostbullet': 400,
    'smallthunder': 5000,
    'boulder': 5000,
    'magicshield': 20000,
    'selfheal': 10000,
    'bard': 500,
    'freeze': 6000
    }

SPELL_COST = {
    'fireball': 30,
    'smallfire': 90,
    'frostbullet': 40,
    'smallthunder': 80,
    'boulder': 90,
    'magicshield': 300,
    'selfheal': 300,
    'bard': 20,
    'freeze': 150
    }

SPELL_SHEETS = {
    'fireball_right': 'resources/images/fireball_right_54x26.png',
    'fireball_left': 'resources/images/fireball_left_54x26.png',
    'smallfire': 'resources/images/fire_64x64.png',
    'frostbullet_right': 'resources/images/frostbullet_right_64x13.png',
    'frostbullet_left': 'resources/images/frostbullet_left_64x13.png',
    'smallthunder': 'resources/images/thunder_98x203.png',
    'boulder': 'resources/images/boulder_64x64.png',
    'selfheal': 'resources/images/selfheal_127x212.png',
    'magicshield': 'resources/images/magicshield_128x128.png',
    'bard_1': 'resources/images/bard1_150x150.png',
    'bard_2': 'resources/images/bard2_150x150.png',
    'bard_3': 'resources/images/bard3_150x150.png',
    'freeze': 'resources/images/freeze2.png',
    'collision_explosion': 'resources/images/collision_explosion_100x60.png'
    }

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 500, 20),
                 (125, HEIGHT - 350, 600, 20),
                 (350, 200, 100, 30),
                 (1200, 520, 20, 20),
                 (1300, 530, 20, 20),
                 (175, 100, 500, 20),
                 (800, 200, 100, 100),
                 (450, HEIGHT - 50, 10000, 5)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
GRAY = (125, 125, 125)


# Boosters
BOOSTERS_SHEETS = {
    'health': 'resources/images/heart.png',
    'mana': 'resources/images/mana.png',
    'boost_damage': 'resources/images/booster_damage.png',
    'boost_defense': 'resources/images/booster_defense.png',
    'boost_player_speed': 'resources/images/booster_player_speed.png',
    'boost_accuracy': 'resources/images/booster_accuracy.png'
    }

# ustawienia ilości klatek w animacji boosterów
ANIM = {
    'boost_damage': [8, 8, 61],
    'boost_defense': [8, 8, 61],
    'boost_player_speed': [10, 10, 91],
    'boost_accuracy': [8, 8, 61]
    }

# Ustawienie wartości zebranych boosterów
BOOSTERS_VALUE = {
    'damage': 10,
    'defense': 20,
    'player_speed': 5,
    'accuracy': 0.05
}

# Ustawienia oscylacji boostera
BOB_RANGE = 20
BOB_SPEED = 0.8

# folders
IMAGES = 'resources/images'
SOUNDS = 'resources/sounds'