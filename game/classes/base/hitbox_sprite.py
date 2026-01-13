from __future__ import annotations
from abc import ABC

import pygame as pg

from .base_sprite import BaseSprite


class HitboxSprite(BaseSprite, ABC):
    hitbox: pg.Rect

    def __init__(self, sprite_groups, assets, pos):
        super().__init__(sprite_groups, assets, pos)

        self.hitbox = None

    def _check_hitbox_collision(
            self, sprite: HitboxSprite, collidable: HitboxSprite
            ):
        is_colliding = sprite.hitbox.colliderect(collidable.hitbox)
        return is_colliding
    
    def _init_hitbox(self, size, pos):
        self.hitbox = pg.Rect(0, 0, *size)
        self.hitbox.center = pos