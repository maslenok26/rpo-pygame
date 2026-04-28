from __future__ import annotations

from .constants import Layer, AssetType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..types import StatsLeaf

PLAYER: StatsLeaf = {
    'general': {
        'faction': 'player',
        'hp': 100
        },
    'physics': {
        'hitbox_size': (10, 14),
        'speed': 120,
        'dash_speed': 300
        },
    'render': {
        'layer': Layer.PLAYER,
        'asset_path': 'player',
        'asset_type': AssetType.SINGLE
        },
    'components': {
        'timers': {
            'dash': {'duration': 150, 'cooldown': 500}
        },
        'start_weapon_keys': ('revolver', 'shotgun')
    }
}