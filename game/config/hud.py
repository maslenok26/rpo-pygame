from .constants import AssetType, Anchor
from .merger import Tree

HUD = Tree(
    content={
        'hp_bar': Tree(
            defaults={
                'render': {
                    'asset_type': AssetType.SINGLE,
                    'anchor': Anchor.TOPLEFT
                }
            },
            content={
                'outer': {
                    'render': {
                        'anchor_offset': (10, 10)
                    }
                },
                'inner': {
                    'render': {
                        'anchor_offset': (27, 15)
                    }
                }
            }
        )
    }
).merge_defaults(asset_path='hud')