from __future__ import annotations

from .core import TILE_SIZE

from typing import TYPE_CHECKING
if TYPE_CHECKING: 
    from ..types import Stats

WALL: Stats = {
    'physics': {
        'hitbox_size': (TILE_SIZE, TILE_SIZE)
    },
    'render': {
        'asset_path': 'walls.tops'
    }
}

WALL_FACE: Stats = {
    'render': {
        'asset_path': 'walls.face'
    }
}