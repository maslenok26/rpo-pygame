# ПАРАМЕТРЫ РАЗРЕШЕНИЯ
GAME_WIDTH = 320
GAME_HEIGHT = 180
HEIGHTS = { 'HD': 720, 'FHD': 1080, 'QHD': 1440, 'UHD': 2160 }
RESOLUTION = 'HD'
START_SCALE = HEIGHTS[RESOLUTION] // GAME_HEIGHT
START_SCREEN_WIDTH = GAME_WIDTH * START_SCALE
START_SCREEN_HEIGHT = GAME_HEIGHT * START_SCALE

# ПАРАМЕТРЫ СПРАЙТОВ
TILE_SIZE = 16

# ПАРАМЕТРЫ ФИЗИКИ
SUB_STEP = 1

# ПАРАМЕТРЫ СМЕНЫ КАДРОВ
FPS_LOCK = True
FPS = 60

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