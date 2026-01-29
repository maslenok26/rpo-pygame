from __future__ import annotations
from typing import Callable

import pygame as pg

from .. import Timer
from ... import config as cfg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...types import SpriteGroups, Assets, StatsLeaf


class BaseSprite(pg.sprite.Sprite):
    _sprite_groups: SpriteGroups
    _assets: Assets
    image_idx = 0

    def __init__(self, sprite_groups, assets, pos, stats: StatsLeaf):
        super().__init__()

        self._sprite_groups = sprite_groups
        self._assets = assets

        self.rect = pg.Rect(*pos, 0, 0)
        render = stats.get('render')
        if render:
            if 'layer' in render:
                self._layer = render['layer']
                self._add_to_groups('rendering')
            self.asset_path = render['asset_path']
            self.orig_image = self._get_asset()[self.image_idx]
            self._set_image(self.orig_image)

    def _get_asset(self):
        current = self._assets
        for key in self.asset_path.split('.'):
            current = current[key]
        return current

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
        shadow_assets = self._assets['shadows']
        shadow_key = self.asset_path.replace('.', '-')
        if shadow_key not in shadow_assets:
            shadow_assets[shadow_key] = gen_func(self.image)
        shadow_stats: StatsLeaf = {
            'render': {
                'layer': cfg.LAYERS['shadow'],
                'asset_path': f'shadows.{shadow_key}'
            }
        }
        return shadow_stats