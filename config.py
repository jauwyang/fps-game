# ===== CONSTANT SETTINGS ======
#  Display Dimensions
WINDOW_HEIGHT = 750
WINDOW_WIDTH = 1200
SCENE_HEIGHT = 750
SCENE_WIDTH = 1200
MAP_WIDTH = WINDOW_WIDTH - SCENE_WIDTH
MAP_HEIGHT = 900

#  Map Dimensions
PLAYABLE_MAP_SIZE = 1080

#  Map Scales
PLAYABLE_TO_MAP_SCREEN_SCALE = MAP_HEIGHT / PLAYABLE_MAP_SIZE

#  Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (45, 45, 48)

# Other
ENEMY_HITBOX_WIDTH = 12
PISTOL_COOLDOWN = 10

# ===== CUSTOMIZALE SETTINGS =====
#  Crosshair Settings
CROSSHAIR_LENGTH = 14
CROSSHAIR_WIDTH = 2
CROSSHAIR_COLOUR = GREEN

#  Game Settings
FOV = 80
ENEMY_NUM = 1
LIMITED_VISION = False
DEBUG_MAP_VIEW = False
MAP_DIVISION = 3
MAX_ENEMIES = 4