from abc import ABC

import pygame as pg


class HitboxSprite(pg.sprite.Sprite, ABC):
    def __init__(self, sprite_groups):
        super().__init__(sprite_groups)

        self.rect: pg.Rect = None

        self.hitbox: pg.Rect = None

    def _check_hitbox_collision(
            self, sprite: 'HitboxSprite', collidable: 'HitboxSprite'
            ):
        is_colliding = sprite.hitbox.colliderect(collidable.hitbox)
        return is_colliding