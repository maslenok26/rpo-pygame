from __future__ import annotations

from .constants import Layer, AssetType
from .merger import Tree

ENEMIES = Tree(
    defaults={
        'general': {
            'faction': 'enemy'
        },
        'render': {
            'layer': Layer.ENEMY,
            'asset_type': AssetType.SINGLE
        }
    },
    content={
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
).merge_defaults(asset_path='enemies')