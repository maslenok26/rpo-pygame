from __future__ import annotations

from .core import LAYERS
from ..utils import config

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..types import StatsLeaf

ENEMIES: dict[str, StatsLeaf] = config({
    'default': {
        'general': {
            'faction': 'enemy'
        },
        'render': {
            'layer': LAYERS['enemy']
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
            'speed': 50,
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
})