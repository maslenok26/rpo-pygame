from __future__ import annotations
from typing import Callable

import pygame as pg

from .. import Timer
from ... import config as cfg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...types import SpriteGroups, StatsLeaf


class BaseSprite(pg.sprite.Sprite):
    _sprite_groups: SpriteGroups
    _assets: dict[str, pg.Surface | tuple[pg.Surface, ...]]
    image_idx = 0

    def __init__(self, sprite_groups, assets, pos, stats: StatsLeaf):
        super().__init__()

        self._sprite_groups = sprite_groups
        self._assets = assets

        self.rect = pg.Rect(*pos, 0, 0)
        render = stats.get('render')
        if render is None: return
        if cfg.CfgKey.Render.LAYER in render:
            self._layer = render['layer']
            self._add_to_groups('rendering')
        self.asset_path = render['asset_path']
        asset = self._assets[self.asset_path]
        match render['asset_type']:
            case cfg.AssetType.SINGLE:
                self.orig_image = asset
            case cfg.AssetType.TUPLE:
                self.orig_image = asset[self.image_idx]
            case _:
                raise ValueError('Неизвестный тип ассета')
        self._set_image(self.orig_image)

    def _set_image(self, image: pg.Surface):
        self.image = image
        self.rect.size, self.rect.center = image.size, self.rect.center

    def _init_timers(self, stats: StatsLeaf, **end_funcs):
        self.timers = {
            key: Timer(**stats['components']['timers'][key], end_func=end_func)
            for key, end_func in end_funcs.items()
        }

    def _update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def _add_to_groups(self, *keys):
        for key in keys:
            sprite_group: pg.sprite.AbstractGroup = self._sprite_groups[key]
            sprite_group.add(self)

    def _get_shadow_stats(
            self, gen_func: Callable[[pg.Surface], pg.Surface]
            ):
        shadow_asset_path = (
            cfg.SHADOW_PREFIX + cfg.ASSET_PATH_SEP + self.asset_path
        )
        self._assets.setdefault(shadow_asset_path, gen_func(self.image))
        shadow_stats: StatsLeaf = {
            'render': {
                'layer': cfg.Layer.SHADOW,
                'asset_path': shadow_asset_path,
                'asset_type': cfg.AssetType.SINGLE
            }
        }
        return shadow_stats