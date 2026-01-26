from __future__ import annotations
from abc import ABC
from typing import Callable

import pygame as pg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...types import SpriteGroups, Assets, Stats


class BaseSprite(pg.sprite.Sprite, ABC):
    _sprite_groups: SpriteGroups
    _assets: Assets
    _layer: int | None = None
    image_idx = 0

    def __init__(self, sprite_groups, assets, pos, stats: Stats):
        super().__init__()

        self._sprite_groups = sprite_groups
        self._assets = assets

        self.rect = pg.Rect(*pos, 0, 0)
        self.asset_path = stats['render']['asset_path']
        self.orig_image = self._get_asset(self.asset_path)[self.image_idx]
        self._set_image(self.orig_image)

    def _get_asset(self, path: str):
        current = self._assets
        for key in path.split('.'):
            current = current[key]
        return current

    def _set_image(self, image: pg.Surface):
        self.image = image
        self.rect.size, self.rect.center = image.size, self.rect.center

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
        shadow_stats: Stats = {
            'render': {
                'asset_path': f'shadows.{shadow_key}'
            }
        }
        return shadow_stats