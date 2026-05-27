from __future__ import annotations

import pygame as pg

from .world_sprite import WorldSprite


class HitboxSprite(WorldSprite):
    def __init__(self, sprite_groups, assets, pos, stats):
        super().__init__(sprite_groups, assets, pos, stats)

        self._physics = self._stats['physics']

        self.hitbox = pg.Rect((0, 0), self._physics['hitbox_size'])
        self.hitbox.center = pos

    def _check_hitbox_collision(
            #  метод для аргумента collided в pg.sprite.spritecollide, поэтому три аргумента
            self, sprite: HitboxSprite, collidable: HitboxSprite 
            ):
        is_colliding = sprite.hitbox.colliderect(collidable.hitbox)
        return is_colliding