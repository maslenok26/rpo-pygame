from enum import Enum, IntEnum, StrEnum, auto

import pygame as pg

# РАЗРЕШЕНИE
GAME_WIDTH = 320
GAME_HEIGHT = 240
START_SCREEN_SIZE = (1280, 720)
LETTERBOXING = True
TILE_SIZE = 16

# СМЕНА КАДРОВ
FPS_LOCK = True
FPS = 60
GAME_SURF_CENTER = pg.Vector2(GAME_WIDTH/2, GAME_HEIGHT/2)

# ФИЗИКА
SUB_STEP_LIMIT = 10
EPSILON = 1e-3

class CollisionAction(Enum):
    STOP = auto()
    PASS = auto()
    BOUNCE = auto()
    KILLSELF = auto()

# ОТРИСОВКА
class Layers(IntEnum):
    SHADOW = 0
    WALL_FACE = 1
    ENEMY = 3
    PLAYER = 7
    PROJECTILE = 9
    WALL_TOP = 10

BG_WALL_COLOR = (58, 68, 102)

# ЗАГРУЗКА АССЕТОВ
class AssetType(Enum):
    SINGLE = auto()
    TUPLE = auto()

class AssetPathSep(StrEnum):
    MAIN = '.'
    ALT = '/'

ASSET_SUFFIX = '.png'
SEQUENCE_SUFFIX = '.seq'

# ГЕНЕРАЦИЯ КАРТЫ
class GameObject(Enum):
    FLOOR = auto()
    WALL = auto()
    PLAYER = auto()
    ENEMY = auto()