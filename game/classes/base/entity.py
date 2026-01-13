from __future__ import annotations
from abc import ABC

import pygame as pg

from .body import Body

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .hitbox_sprite import HitboxSprite
    from ..weapon import Weapon


class Entity(Body, ABC):
    collidables: pg.sprite.Group[HitboxSprite]
    weapon: Weapon

    def __init__(self, sprite_groups, assets, pos):
        super().__init__(sprite_groups, assets, pos)

        self.hp = 0
        self.is_dead = False

        self.image_flipped = False

        self.collidables = self.sprite_groups['obstacles']

        self.look_vec = pg.Vector2(1, 0)

        self.weapon = None

    def take_damage(self, amount):
        if self.is_dead: return
        self.hp -= amount
        if self.hp <= 0:
            self.die()
    
    def die(self):
        self.is_dead = True
        self.weapon.kill()
        self.kill()

    def _handle_collision(self, _):
        return 'STOP'

    def _flip_image(self):
        if ((self.look_vec.x < 0 and not self.image_flipped)
            or (self.look_vec.x > 0 and self.image_flipped)):
            self.image = pg.transform.flip(
                self.image, flip_x=True, flip_y=False
                )
            self.image_flipped = not self.image_flipped