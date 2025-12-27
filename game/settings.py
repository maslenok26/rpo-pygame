# ПАРАМЕТРЫ РАЗРЕШЕНИЯ
TILE_SIZE = 8
GAME_WIDTH = TILE_SIZE * 40
GAME_HEIGHT = TILE_SIZE * 22.5
HEIGHTS = { 'HD': 720, 'FHD': 1080, 'QHD': 1440, 'UHD': 2160 }
RESOLUTION = 'HD'
START_SCALE = HEIGHTS[RESOLUTION] // GAME_HEIGHT
START_SCREEN_WIDTH = GAME_WIDTH * START_SCALE
START_SCREEN_HEIGHT = GAME_HEIGHT * START_SCALE

# ПАРАМЕТРЫ СМЕНЫ КАДРОВ
FPS_LOCK = True
FPS = 60

# ПАРАМЕТРЫ ФИЗИКИ
SUB_STEP = 1

# ТЕСТОВАЯ КАРТА
TEST_MAP = [
    'W W W W W W W W W W W W W W W W W W W W',
    '. . . . . . . . . . . . . . . . . . . W',
    '. . . . . . . . . . . . . . . . . . . W',
    'W . . . . P . . . W . . . . . . . . . W',
    'W . . . . . . . . W . . . . . . . . . W',
    'W . . . . . W W W W W W W . . . . . . W',
    'W . . . . . . . . . . . W . . . . . . W',
    'W . . . . . . . . . . . W . . . . . . W',
    'W . . . . . . . . . . . W . . . . . . W',
    'W . . . . . . . . . . . . . . . . . . W',
    'W . . . . . . . . . . . . . . . . . . W',
    'W W W W W W W W W W W W W W W W W W W W'
]