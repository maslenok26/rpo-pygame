from __future__ import annotations

from .core import TILE_SIZE, LAYERS

from typing import TYPE_CHECKING
if TYPE_CHECKING: 
    from ..types import StatsLeaf

WALL: StatsLeaf = {
    'physics': {
        'hitbox_size': (TILE_SIZE, TILE_SIZE)
    },
    'render': {
        'layer': LAYERS['wall_top'],
        'asset_path': 'walls.tops',
        'y_offset': 4
    }
}

WALL_FACE: StatsLeaf = {
    'render': {
        'layer': LAYERS['wall_face'],
        'asset_path': 'walls.face'
    }
}