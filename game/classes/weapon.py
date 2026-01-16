from __future__ import annotations
from math import copysign

import pygame as pg

from . import BaseSprite
from .timer import Timer
from .projectile import Projectile

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Entity


class Weapon(BaseSprite):
    orig_image: pg.Surface
    owner: Entity
    proj_self_group_key: str
    proj_target_group_keys: tuple[str]

    def __init__(self, sprite_groups, assets,
                 owner: Entity, proj_self_group_key, proj_target_group_keys):
        super().__init__(sprite_groups, assets, owner.rect.center)

        self._orig_layer = owner._layer
        self._layer = self._orig_layer
        self.add_to_groups('rendering')

        self.orbit_offset = pg.Vector2(3, 4)
        self.muzzle_offset = pg.Vector2(18, -3)
        self.cur_orbit_offset = self.orbit_offset.copy()
        self.cur_muzzle_offset = self.muzzle_offset.copy()

        self.orig_image = self.assets['shotgun']
        self.image = self.set_image(self.orig_image)
        self.vector = owner.look_vec.copy()
        self.stable_angle = 0

        self.timers = {
            'shoot': Timer(
                duration=0, end_func=None, cooldown=300
            )
        }

        self.owner = owner
        self.proj_self_group_key = proj_self_group_key
        self.proj_target_group_keys = proj_target_group_keys

    def update(self, vector):
        self.rect.center = self.owner.rect.center
        self._rotate(vector)
        self.timers['shoot'].update()

    def animate(self):
        self._rotate_image()

    def shoot(self):
        if not self.timers['shoot'].start(): return
        spawn_pos = self.rect.center + self.cur_muzzle_offset
        Projectile(
            self.sprite_groups, 
            self.assets,
            spawn_pos,
            self.vector.copy(),
            self.proj_self_group_key,
            self.proj_target_group_keys
        )

    def _rotate(self, vector: pg.Vector2):
        self.vector = vector
        cur_angle = self.vector.angle
        if abs(cur_angle) != 90:
            self.stable_angle = cur_angle
        self.cur_orbit_offset = self.orbit_offset.copy()
        self.cur_muzzle_offset = self.muzzle_offset.copy()
        should_flip = abs(self.stable_angle) > 90
        if should_flip:
            self.cur_orbit_offset.y *= -1
            self.cur_muzzle_offset.y *= -1
        self.cur_orbit_offset.rotate_ip(cur_angle)
        self.cur_muzzle_offset.rotate_ip(cur_angle)
        self.rect.center += self.cur_orbit_offset

    def _rotate_image(self):
        angle = self.vector.angle
        image_to_rotate = self.orig_image
        if self.owner.image_flipped:
            image_to_rotate = pg.transform.flip(
                image_to_rotate, flip_x=False, flip_y=True
                )
        self.image = pg.transform.rotate(image_to_rotate, -angle)
        layer_offset = copysign(1, angle)
        new_layer = self._orig_layer + layer_offset
        if new_layer != self._layer:
            self.sprite_groups['rendering'].change_layer(self, new_layer)
        self.rect = self.image.get_rect(center=self.rect.center)