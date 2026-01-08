from __future__ import annotations
from abc import ABC

import pygame as pg

from .base_sprite import BaseSprite


class HitboxSprite(BaseSprite, ABC):
    def __init__(self, sprite_groups):
        super().__init__(sprite_groups)

        self.hitbox: pg.Rect = None

    def _check_hitbox_collision(
            self, sprite: HitboxSprite, collidable: HitboxSprite
            ):
        is_colliding = sprite.hitbox.colliderect(collidable.hitbox)
        return is_colliding
    
    def _init_hitbox(self, width, height, *pos):
        self.hitbox = pg.Rect(0, 0, width, height)
        self.hitbox.center = pos