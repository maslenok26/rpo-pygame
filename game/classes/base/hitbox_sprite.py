from __future__ import annotations
from abc import ABC

import pygame as pg

from .base_sprite import BaseSprite

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...types import StatsLeaf


class HitboxSprite(BaseSprite, ABC):
    def __init__(self, sprite_groups, assets, pos, stats: StatsLeaf):
        super().__init__(sprite_groups, assets, pos, stats)

        self.hitbox = pg.Rect(0, 0, *stats['physics']['hitbox_size'])
        self.hitbox.center = pos

    def _check_hitbox_collision(
            self, sprite: HitboxSprite, collidable: HitboxSprite
            ):
        is_colliding = sprite.hitbox.colliderect(collidable.hitbox)
        return is_colliding