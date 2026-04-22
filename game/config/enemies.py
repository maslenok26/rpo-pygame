from __future__ import annotations

from .core import Layers, AssetType
from ..utils import merge_defaults

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..types import StatsLeaf

ENEMIES: dict[str, StatsLeaf] = {
    'default': {
        'general': {
            'faction': 'enemy'
        },
        'render': {
            'layer': Layers.ENEMY,
            'asset_type': AssetType.SINGLE
        }
        },
    'skeleton': {
        'general': {
            'hp': 30,
            'detection_radius': 120,
            'shoot_radius': 100,
            'stop_radius': 50
        },
        'physics': {
            'hitbox_size': (10, 14),
            'speed': 50
        },
        'render': {
            'asset_path': 'skeleton'
        },
        'components': {
            'timers': {
                'shoot': {'cooldown': 1000}
            },
            'start_weapon_keys': ('revolver',)
        }
    }
}
merge_defaults(ENEMIES)