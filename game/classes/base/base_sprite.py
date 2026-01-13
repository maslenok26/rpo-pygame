from __future__ import annotations
from abc import ABC

import pygame as pg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...types import SpriteGroups, Assets


class BaseSprite(pg.sprite.Sprite, ABC):
    sprite_groups: SpriteGroups
    assets: Assets
    _layer: int | None
    image: pg.Surface | None

    def __init__(self, sprite_groups, assets, pos):
        super().__init__()

        self.sprite_groups = sprite_groups
        self.assets = assets

        self._layer = None

        self.image = None
        self.rect = pg.Rect(*pos, 0, 0)

    def set_image(self, image: pg.Surface):
        self.image = image
        self.rect = image.get_rect(center=self.rect.center)

    def add_to_groups(self, *names):
        for name in names:
            sprite_group: pg.sprite.AbstractGroup = self.sprite_groups[name]
            sprite_group.add(self)