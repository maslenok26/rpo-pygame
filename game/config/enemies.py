from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..types import StatsDict

ENEMIES: StatsDict = {
    'enemy': {
        'general': {
            'faction': 'enemy',
            'hp': 100,
            'detection_radius': 120,
            'shoot_radius': 100,
            'stop_radius': 40
        },
        'physics': {
            'hitbox_size': (10, 14),
            'speed': 50,
        },
        'render': {
            'asset_path': 'enemy'
        },
        'components': {
            'timers': {
                'shoot': {'cooldown': 1000}
            },
            'start_weapon_keys': ('pistol',)
        }
    }
}