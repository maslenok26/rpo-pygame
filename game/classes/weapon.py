from __future__ import annotations
from math import copysign

import pygame as pg

from . import BaseSprite
from .timer import Timer
from .projectile import Projectile
from .. import config as cfg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Entity


class Weapon(BaseSprite):
    orig_image: pg.Surface
    image: pg.Surface
    owner: Entity
    proj_self_group_key: str
    proj_target_group_keys: tuple[str]

    def __init__(
            self,
            sprite_groups, assets,
            type_key,
            owner: Entity, faction,
            ):
        super().__init__(sprite_groups, assets, owner.rect.center)

        self._orig_layer = owner._layer
        self._layer = self._orig_layer
        self.add_to_groups('rendering')

        stats = cfg.WEAPON_STATS[type_key]

        self.orbit_offset = pg.Vector2(stats['orbit_offset'])
        self.muzzle_offset = pg.Vector2(stats['muzzle_offset'])
        self._cur_orbit_offset = self.orbit_offset.copy()
        self._cur_muzzle_offset = self.muzzle_offset.copy()
        self.holstered_offset = pg.Vector2(stats['holstered_offset'])
        self.holstered_angle = -110
        self.is_active = True

        self.orig_image = self._assets[type_key]
        self.holstered_image = pg.transform.rotate(
            self.orig_image, -self.holstered_angle
            )
        self.set_image(self.orig_image)
        self.vector = owner.look_vec

        self.timers = {
            'shoot': Timer(cooldown=stats['cooldown'])
        }

        self.owner = owner
        self.combat_rules = cfg.COMBAT_RULES[faction]
        self.proj_type_key = stats['proj_type_key']
        self.proj_stats = stats['proj_stats']

    def update(self):
        self._sync_with_owner()
        if self.is_active:
            self._rotate()
        self.timers['shoot'].update()

    def animate(self):
        if self.is_active:
            self._rotate_image_active()
        else:
            self._rotate_image_holstered()

    def equip(self):
        self.is_active = True
        self._sync_with_owner()
        self._layer = self._orig_layer
        self._rotate()

    def unequip(self):
        self.is_active = False
        self._sync_with_owner()
        self._layer = self._orig_layer - 2
        self._sprite_groups['rendering'].change_layer(self, self._layer)

    def shoot(self):
        if not self.timers['shoot'].start(): return
        spawn_pos = self.rect.center + self._cur_muzzle_offset
        Projectile(
            self._sprite_groups, self._assets, spawn_pos,
            self.proj_type_key,
            self.vector,
            self.combat_rules['proj_self_group_key'],
            self.combat_rules['proj_target_group_keys'],
            self.proj_stats
        )

    def _sync_with_owner(self):
        self.rect.center = self.owner.rect.center

    def _rotate(self):
        cur_angle = self.vector.angle
        self._cur_orbit_offset = self.orbit_offset.copy()
        self._cur_muzzle_offset = self.muzzle_offset.copy()
        should_flip = abs(cur_angle) > 90
        if should_flip:
            self._cur_orbit_offset.y *= -1
            self._cur_muzzle_offset.y *= -1
        self._cur_orbit_offset.rotate_ip(cur_angle)
        self._cur_muzzle_offset.rotate_ip(cur_angle)
        self.rect.center += self._cur_orbit_offset

    def _rotate_image_active(self):
        angle = self.vector.angle
        if self.owner.image_flipped:
            image_to_rotate = pg.transform.flip(
                self.orig_image, flip_x=False, flip_y=True
                )
        else:
            image_to_rotate = self.orig_image
        self.set_image(pg.transform.rotate(image_to_rotate, -angle))
        layer_offset = copysign(1, angle)
        new_layer = self._orig_layer + layer_offset
        if new_layer != self._layer:
            self._sprite_groups['rendering'].change_layer(self, new_layer)

    def _rotate_image_holstered(self):
        offset = self.holstered_offset.copy()
        if self.owner.image_flipped:
            self.set_image(pg.transform.flip(
                self.holstered_image, flip_x=True, flip_y=False
                ))
            offset.x *= -1
        else:
            self.set_image(self.holstered_image)
        self.rect.center += offset