from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..types import Stats

PLAYER: Stats = {
    'general': {
        'faction': 'player',
        'hp': float('inf')
        },
    'physics': {
        'hitbox_size': (10, 14),
        'speed': 135,
        'dash_speed': 300
        },
    'render':{
        'asset_path': 'player'
        },
    'components': {
        'timers': {
            'dash': {'duration': 150, 'cooldown': 500}
        },
        'start_weapon_keys': ('pistol', 'shotgun')
    }
}