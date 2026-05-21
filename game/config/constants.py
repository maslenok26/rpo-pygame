from enum import Enum, IntEnum, StrEnum, auto

import pygame as pg

# РАЗРЕШЕНИE
GAME_SURF_SIZE = pg.Vector2(320, 240)
START_SCREEN_SIZE = (1280, 720)
LETTERBOXING = True
TILE_SIZE = 16

GAME_SURF_CENTER = GAME_SURF_SIZE / 2

# СМЕНА КАДРОВ
FPS_LOCK = True
FPS = 60
VSYNC = True

# ФИЗИКА
SUB_STEP_LIMIT = 10
EPSILON = 1e-3

class CollisionAction(Enum):
    STOP = auto()
    PASS = auto()
    BOUNCE = auto()
    KILLSELF = auto()

# ОТРИСОВКА
class Layer(IntEnum):
    SHADOW = 0
    WALL_FACE = 1
    # 2: оружие врага (угол < 0°)
    ENEMY = 3
    # 4: оружие врага (угол >= 0°)
    # 5: оружие за спиной игрока
    # 6: оружие игрока (угол < 0°)
    PLAYER = 7
    # 8: оружие игрока (угол >= 0°)
    PROJECTILE = 9
    WALL_TOP = 10

class Anchor(Enum):
    TOPLEFT = auto()
    TOPRIGHT = auto()
    BOTTOMLEFT = auto()
    BOTTOMRIGHT = auto()

ANCHORS_NORM_OFFSETS = {
    Anchor.TOPLEFT: (0, 0),
    Anchor.TOPRIGHT: (1, 0),
    Anchor.BOTTOMLEFT: (0, 1),
    Anchor.BOTTOMRIGHT: (1, 1)
}

BG_WALL_COLOR = (58, 68, 102)

# ЗАГРУЗКА АССЕТОВ
class AssetType(Enum):
    SINGLE = auto()
    SEQUENCE = auto()

ASSET_PATH_SEP = '.'

ASSET_SUFFIX = '.png'
SEQUENCE_SUFFIX = '.seq'

SHADOW_PREFIX = 'shadow'
SHADOW_COLOR = (20, 24, 37, 130)

# ГЕНЕРАЦИЯ КАРТЫ
class GameObject(Enum):
    FLOOR = auto()
    WALL = auto()
    PLAYER = auto()
    ENEMY = auto()

# КОНФИГИ
class CfgKey:
    class Leaf(StrEnum):
        GENERAL = 'general'
        RENDER = 'render'
        PHYSICS = 'physics'
        COMPONENTS = 'components'

    class Render(StrEnum):
        LAYER = 'layer'