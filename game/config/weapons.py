from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..types import FactionRule, StatsDict

FACTION_RULES: dict[str, FactionRule] = {
    'player': {
        'proj_self_group_key': 'player_projectiles',
        'proj_target_group_keys': ('enemies', 'player')
    },
    'enemy': {
        'proj_self_group_key': 'enemy_projectiles',
        'proj_target_group_keys': ('player',)
    }
}

WEAPONS: StatsDict = {
    'pistol': {
        'general': {
            'orbit_offset': (8, 3),
            'muzzle_offset': (9, -2),
            'holstered_offset': (-5, -8),
            'proj_stats': {
                'general': {
                    'damage': 10
                },
                'physics': {
                    'hitbox_size': (4, 4),
                    'speed': 150
                },
                'render': {
                    'asset_path': 'projectile'
                },
                'components': {
                    'timers': {
                        'lifetime': {'duration': 3000}
                    }
                }
            }
        },
        'render': {
            'asset_path': 'pistol'
        },
        'components': {
            'timers': {
                'shoot': {'cooldown': 150}
            }
        }
    },
    'shotgun': {
        'general': {
            'orbit_offset': (3, 4),
            'muzzle_offset': (19, -2),
            'holstered_offset': (-3, -4),
            'proj_stats': {
                'general': {
                    'damage': 40
                },
                'physics': {
                    'hitbox_size': (4, 4),
                    'speed': 150
                },
                'render': {
                    'asset_path': 'projectile'
                },
                'components': {
                    'timers': {
                        'lifetime': {'duration': 1500}
                    }
                }
            }
        },
        'render': {
            'asset_path': 'shotgun'
        },
        'components': {
            'timers': {
                'shoot': {'cooldown': 300}
            }
        }
    }
}