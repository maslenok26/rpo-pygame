from __future__ import annotations

from .constants import TILE_SIZE, Layer, AssetType

from typing import TYPE_CHECKING
if TYPE_CHECKING: 
    from ..types import StatsLeaf

WALL: StatsLeaf = {
    'physics': {
        'hitbox_size': (TILE_SIZE, TILE_SIZE)
    },
    'render': {
        'layer': Layer.WALL_TOP,
        'asset_path': 'walls.tops',
        'asset_type': AssetType.TUPLE,
        'y_offset': 4   # высота текстуры лица стены / 2
    }
}

WALL_FACE: StatsLeaf = {
    'render': {
        'layer': Layer.WALL_FACE,
        'asset_path': 'walls.wall_face',
        'asset_type': AssetType.SINGLE
    }
}