# game options/settings
TITLE = "PyRarria"
WIDTH = 800
HEIGHT = 600
FPS = 60

# Player properties
PLAYER_ACC = 1
PLAYER_FRICTION = -0.2
PLAYER_GRAV = 0.8
MAX_VEL_Y = 15

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 500, 20),
                 (125, HEIGHT - 350, 600, 20),
                 #(350, 200, 800, 30),
                 (1200, 520, 20, 20),
                 (1300, 530, 20, 20),
                 (175, 100, 500, 20),
                 (450, HEIGHT - 50, 10000,5)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)