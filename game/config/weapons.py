from __future__ import annotations

from .core import LAYERS
from ..utils import config

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..types import FactionRule, StatsLeaf

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

WEAPONS: dict[str, StatsLeaf] = config({
    'default': {
        'general': {
            'proj_stats': {
                'render': {
                    'layer': LAYERS['projectile'],
                    'asset_path': 'projectile'
                    }
                }
            }
        },
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
                    'speed': 230,
                    'drag': 0.15
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
                    'speed': 160,
                    'drag': 0.3
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
})