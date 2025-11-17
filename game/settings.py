TILE_SIZE = 16
GAME_WIDTH = TILE_SIZE * 20
GAME_HEIGHT = TILE_SIZE * 12
FIRST_SCALE = 64 / TILE_SIZE
FIRST_SCREEN_WIDTH = GAME_WIDTH * FIRST_SCALE
FIRST_SCREEN_HEIGHT = GAME_HEIGHT * FIRST_SCALE
WORLD_MAP = [
    'W W W W W W W W W W W W W W W W W W W W',
    '. . . . . . . . . . . . . . . . . . . W',
    '. . . . . . . . . . . . . . . . . . . W',
    'W . . . . P . . . W . . . . . . . . . W',
    'W . . . . . . . . W . . . . . . . . . W', # Тестовая карта
    'W . . . . . W W W W W W W . . . . . . W',
    'W . . . . . . . . . . . W . . . . . . W',
    'W . . . . . . . . . . . W . . . . . . W',
    'W . . . . . . . . . . . W . . . . . . W',
    'W . . . . . . . . . . . . . . . . . . W',
    'W . . . . . . . . . . . . . . . . . . W',
    'W W W W W W W W W W W W W W W W W W W W'
]
SUB_STEP = 1