from abc import ABC

import pygame as pg

from ..types import SpriteGroups


class BaseSprite(pg.sprite.Sprite, ABC):
    sprite_groups: SpriteGroups

    def __init__(self, sprite_groups: SpriteGroups):
        super().__init__()

        self.sprite_groups = sprite_groups

        self._layer: int | None = None

        self.image: pg.Surface | None = None
        self.rect: pg.Rect | None = None

    def add_to_groups(self, *names):
        for name in names:
            sprite_group: pg.sprite.AbstractGroup = self.sprite_groups[name]
            sprite_group.add(self)