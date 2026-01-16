from .types import Layers

# ПАРАМЕТРЫ РАЗРЕШЕНИЯ
GAME_WIDTH = 320
GAME_HEIGHT = 240
HEIGHTS = {'HD': 720, 'FHD': 1080, 'QHD': 1440, 'UHD': 2160}
RESOLUTION = 'HD'
START_SCREEN_WIDTH = HEIGHTS[RESOLUTION] * (16 / 9)
START_SCREEN_HEIGHT = HEIGHTS[RESOLUTION]
LETTERBOXING = True

# ПАРАМЕТРЫ СПРАЙТОВ
TILE_SIZE = 16
LAYERS: Layers = {
    'WALL_FACE': 0,
    'ENEMY': 2,
    'PLAYER': 5,
    'PROJECTILE': 7,
    'WALL_TOP': 8
}

# ПАРАМЕТРЫ ФИЗИКИ
SUB_STEP_LIMIT = 10

# ПАРАМЕТРЫ СМЕНЫ КАДРОВ
FPS_LOCK = True
FPS = 60

# ТЕСТОВАЯ КАРТА
TEST_MAP = [
    'W W W W W W W W W W W W W W W W W W W W ',
    '. . . . . . . . . . . . . . . . . . . W ',
    '. . . . . . . . . . . . . . E . . . . W ',
    'W . . . . P . . . W . . . . . . . . . W ',
    'W . . . . . . . . W . . . . . . . . . W ',
    'W . . . . . W W W W W W W . . . . . . W ',
    'W . . . . . . . . . . . W . . . . . . W ',
    'W . . . . . . . . . . . W . . . . . . W ',
    'W . . . . . . . . . . . W . . . . . . W ',
    'W . . . . . . . . . . . . . . . . . . W ',
    'W . . . . . . . . . . . . . . . . . . W ',
    'W W W W W W W W W W W W W W W W W W W W '
]