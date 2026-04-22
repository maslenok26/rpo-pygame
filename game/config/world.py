from __future__ import annotations

from .core import TILE_SIZE, Layers, AssetType

from typing import TYPE_CHECKING
if TYPE_CHECKING: 
    from ..types import StatsLeaf

WALL: StatsLeaf = {
    'physics': {
        'hitbox_size': (TILE_SIZE, TILE_SIZE)
    },
    'render': {
        'layer': Layers.WALL_TOP,
        'asset_path': 'walls.tops',
        'asset_type': AssetType.TUPLE,
        'y_offset': 4
    }
}

WALL_FACE: StatsLeaf = {
    'render': {
        'layer': Layers.WALL_FACE,
        'asset_path': 'walls.wall_face',
        'asset_type': AssetType.SINGLE
    }
}