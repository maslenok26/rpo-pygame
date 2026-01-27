from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..types import Layers

# ПАРАМЕТРЫ РАЗРЕШЕНИЯ
GAME_WIDTH = 320
GAME_HEIGHT = 240
HEIGHTS = {'HD': 720, 'FHD': 1080, 'QHD': 1440, 'UHD': 2160}
RESOLUTION = 'HD'
START_SCREEN_SIZE = (HEIGHTS[RESOLUTION] * (16 / 9), HEIGHTS[RESOLUTION])
LETTERBOXING = True
TILE_SIZE = 16

# ПАРАМЕТРЫ ФИЗИКИ
SUB_STEP_LIMIT = 10
EPSILON = 1e-3

# ПАРАМЕТРЫ СМЕНЫ КАДРОВ
FPS_LOCK = True
FPS = 60

# ПАРАМЕТРЫ ОТРИСОВКИ
LAYERS: Layers = {
    'shadow': 0,
    'wall_face': 1,
    'enemy': 3,
    'player': 7,
    'projectile': 9,
    'wall_top': 10
}
BG_WALL_COLOR = (58, 68, 102)