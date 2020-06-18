# game options/settings
TITLE = "PyRarria"
WIDTH = 1600
HEIGHT = 1200
FPS = 60

# folders
IMAGES = "resources/images/hud/"
BACKGROUND = "resources/images/backgrounds/"
FOOD = "resources/images/food/"
TOOL = "resources/images/tools/"
TERRAIN = "resources/images/terrain/"
ARMOUR = "resources/images/armour/"
SCREENS = "resources/images/screens/"
SOUNDS = "resources/sounds/"
CREATURES = "resources/images/creatures/"

# Player properties
PLAYER_MOVE = {
    "PLAYER_ACC": 1.2,
    "PLAYER_GRAV": 0.8,
    "PLAYER_FRICTION": -0.2,
    "JUMP_VEL": -20,
    "MAX_VEL_Y": 15,
    "FRICTION": -0.12,
}
PLAYER_VALUES = {"DAMAGE": 0, "DEFENCE": 0, "MANA_REDUCTION": 0, "ACCURACY": 1, "TERRAIN_RANGE": 150}

# Health/Mana bar properties
HEART_VALUE = 195
STAR_VALUE = 195
HEALTH_RECOVERY_VALUE = 0.5
MANA_RECOVERY_VALUE = 0.5
MAX_HEALTH = 20 * HEART_VALUE
MIN_HEALTH = 5 * HEART_VALUE
MAX_MANA = 20 * STAR_VALUE
MIN_MANA = 5 * STAR_VALUE

# Terrain properties
MAP_WIDTH = 13000
BLOCK_SIZE = 24
BLOCK_RENDER_DISTANCE = (int((WIDTH / BLOCK_SIZE) / 2) + 1, int((HEIGHT / BLOCK_SIZE) / 2) + 1)
# BLOCK_RENDER_DISTANCE = (15,15)
NON_COLLISION_OBJECTS = []

# Images
IMAGES_LIST = {
    # Player
    "player": IMAGES + "player.png",
    # GUI
    "heart": IMAGES + "heart.png",
    "mana": IMAGES + "mana.png",
    # Ekuipment
    "eq_square": IMAGES + "eq_square2.png",
    "open_eq": IMAGES + "open_eq2.png",
    "bin": IMAGES + "bin2.png",
    # Screens
    "background": {
        "main": BACKGROUND + "background_moving_main2.png",
        "2": BACKGROUND + "background_moving_second2.png",
    },
    "start_screen": SCREENS + "start_screen.png",
    "game_over_screen": SCREENS + "game_over_screen.png",
    # START ITEMS
    # Food
    "potato": FOOD + "potato.png",
    "bacon": FOOD + "bacon.png",
    # Tools
    "pickaxe_diamond": TOOL + "pickaxe_diamond.png",
    "green_sword": TOOL + "green_sword.png",
    # Armor
    # Helmets
    "helmet_icon_base": ARMOUR + "helmet_icon_base.png",
    "mage_helmet": ARMOUR + "mage_helmet.png",
    "fire_helmet": ARMOUR + "fire_helmet.png",
    "black_helmet": ARMOUR + "black_helmet2.png",
    "black_cat_helmet": ARMOUR + "black_cat_helmet.png",
    # Breastplates
    "breastplate_icon_base": ARMOUR + "breastplate_icon_base.png",
    "mage_breastplate": ARMOUR + "mage_breastplate.png",
    "black_breastplate": ARMOUR + "black_breastplate2.png",
    "fire_breastplate": ARMOUR + "fire_breastplate.png",
    "black_cat_breastplate": ARMOUR + "black_cat_breastplate.png",
    # Boots
    "boots_icon_base": ARMOUR + "boots_icon_base.png",
    "mage_boots": ARMOUR + "mage_boots.png",
    "black_boots": ARMOUR + "black_boots2.png",
    "black_cat_boots": ARMOUR + "black_cat_boots.png",
    "fire_boots": ARMOUR + "fire_boots.png",
    # Blocks
    "dirt": TERRAIN + "dirt.png",
    "bone_dirt": TERRAIN + "bone_dirt.png",
    "flint_dirt": TERRAIN + "flint_dirt.png",
    "stone": TERRAIN + "stone.png",
    "grass": TERRAIN + "grass.png",
    "mushroom_brown": TERRAIN + "mushroom_brown.png",
    "mushroom_red": TERRAIN + "mushroom_red.png",
    "grass_dirt": TERRAIN + "grass_dirt.png",
    "tall_grass": TERRAIN + "tall_grass.png",
    "iron": TERRAIN + "iron_ore.png",
    "copper": TERRAIN + "copper_ore.png",
    "coal_ore": TERRAIN + "coal_ore.png",
    "chrysoprase_clay": TERRAIN + "chrysoprase_clay.png",
    "clay": TERRAIN + "clay.png",
    "diamond1": TERRAIN + "diamond12.png",
    "diamond2": TERRAIN + "diamond22.png",
    "diamond3": TERRAIN + "diamond32.png",
    "log": TERRAIN + "log.png",
    "log_hole": TERRAIN + "log_hole.png",
    "leaves": TERRAIN + "leaves.png",
    "apple_leaves": TERRAIN + "apple_leaves.png",
    "damaged_1": TERRAIN + "damaged_1.png",
    "damaged_2": TERRAIN + "damaged_2.png",
    "damaged_3": TERRAIN + "damaged_3.png",
    "glass": TERRAIN + "glass.png",
    "cloud": TERRAIN + "cloud.png",
    # END ITEMS
    # Spells
    "smallfire": IMAGES + "smallfire.png",
    "smallthunder": IMAGES + "smallthunder.png",
    "boulder": IMAGES + "boulder.png",
    "magicshield": IMAGES + "magicshield.png",
    "selfheal": IMAGES + "selfheal.png",
    "bard": IMAGES + "bard.png",
    "freeze": IMAGES + "freeze.png",
    "blank": IMAGES + "blank.png",
    "fireball": IMAGES + "fireball.png",
    "frostbullet": IMAGES + "frostbullet.png",
}

SPELL_DELAYS = {
    "fireball": 400,
    "smallfire": 5000,
    "frostbullet": 400,
    "smallthunder": 5000,
    "boulder": 5000,
    "magicshield": 20000,
    "selfheal": 10000,
    "bard": 500,
    "freeze": 6000,
}

SPELL_COST = {
    "fireball": 30,
    "smallfire": 90,
    "frostbullet": 40,
    "smallthunder": 80,
    "boulder": 90,
    "magicshield": 300,
    "selfheal": 300,
    "bard": 20,
    "freeze": 150,
}

SPELL_DURATION = {
    "smallfire": 4000,
    "smallthunder": 720,
    "boulder": 1500,
    "freeze": 15000,
    "magicshield": 60000,
    "fireball": 4000,
    "frostbullet": 3000,
    "frostbullet_freeze": 5000,
}

SPELL_VALUE = {
    "selfheal": 200,
    "magicshield": 10,
    "bard": 1.0,
    "fireball": 50,
    "frostbullet": 30,
    "frostbullet_range": 70,
    "freeze_range": 200,
}

SPELLS_NORMAL_NAME = {
    "fireball": "FireBall",
    "smallfire": "SmallFire",
    "frostbullet": "FrostBullet",
    "smallthunder": "SmallThunder",
    "boulder": "Boulder",
    "magicshield": "MagicShield",
    "selfheal": "SelfHeal",
    "bard": "Bard",
    "freeze": "Freeze",
}

SPELL_SHEETS = {
    "fireball_right": IMAGES + "fireball_right_54x26.png",
    "fireball_left": IMAGES + "fireball_left_54x26.png",
    "smallfire": IMAGES + "fire_64x64.png",
    "frostbullet_right": IMAGES + "frostbullet_right_64x13.png",
    "frostbullet_left": IMAGES + "frostbullet_left_64x13.png",
    "smallthunder": IMAGES + "thunder_98x203.png",
    "boulder": IMAGES + "boulder_64x64.png",
    "selfheal": IMAGES + "selfheal_127x212.png",
    "magicshield": IMAGES + "magicshield_128x128.png",
    "bard_1": IMAGES + "bard1_150x150.png",
    "bard_2": IMAGES + "bard2_150x150.png",
    "bard_3": IMAGES + "bard3_150x150.png",
    "freeze": IMAGES + "freeze2.png",
    "collision_explosion": IMAGES + "collision_explosion_100x60.png",
}

# define some colors
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
    "health": IMAGES + "heart.png",
    "mana": IMAGES + "mana.png",
    "damage_booster": IMAGES + "booster_damage.png",
    "defense_booster": IMAGES + "booster_defense.png",
    "speed_booster": IMAGES + "booster_player_speed.png",
    "accuracy_booster": IMAGES + "booster_accuracy.png",
}

BOOSTERS_DURATIONS = {
    "damage_booster": 10000,
    "defense_booster": 15000,
    "speed_booster": 10000,
    "accuracy_booster": 15000,
}

# ustawienia ilości klatek w animacji boosterów
ANIM = {
    "damage_booster": [8, 8, 61],
    "defense_booster": [8, 8, 61],
    "speed_booster": [10, 10, 91],
    "accuracy_booster": [8, 8, 61],
}

# Ustawienie wartości zebranych boosterów
BOOSTERS_VALUE = {"damage": 10, "defense": 20, "speed": 1, "accuracy": 0.05}

# Ustawienia oscylacji boostera
BOB_RANGE = 20
BOB_SPEED = 0.8
