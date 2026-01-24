from __future__ import annotations
from abc import ABC

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
        self.orig_image = self._get_asset(
            stats['render']['asset_path']
            )[self.image_idx]
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