from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..types import FactionRule, Stats

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

WEAPONS: dict[str, Stats] = {
    'revolver': {
        'general': {
            'orbit_offset': (8, 3),
            'muzzle_offset': (9, -2),
            'holstered_offset': (-5, -8),
            'proj_amount': 1,
            'spread_angle': 15,
            'proj_stats': {
                'general': {
                    'damage': 10,
                    'bounces_left': 0
                },
                'physics': {
                    'hitbox_size': (4, 4),
                    'speed': 200,
                    'drag': 0.15
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
            'asset_path': 'weapons.revolver'
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
            'proj_amount': 5,
            'spread_angle': 40,
            'proj_stats': {
                'general': {
                    'damage': 8,
                    'bounces_left': 2
                },
                'physics': {
                    'hitbox_size': (4, 4),
                    'speed': 150,
                    'drag': 0.3
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
            'asset_path': 'weapons.shotgun'
        },
        'components': {
            'timers': {
                'shoot': {'cooldown': 750}
            }
        }
    }
}