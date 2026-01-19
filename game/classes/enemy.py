from __future__ import annotations
from math import copysign

from . import Entity
from .weapon import Weapon
from .. import config as cfg

import pygame as pg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player


class Enemy(Entity):
    target: Player | None

    def __init__(self, sprite_groups, assets, pos):
        super().__init__(sprite_groups, assets, pos)

        self._layer = cfg.LAYERS['ENEMY']
        self.add_to_groups('rendering', 'enemies')

        self.hp = 100
        self.speed = 45
        self.detection_radius = 140
        self.shoot_radius = 110
        self.stop_radius = 60

        self.set_image(self.assets['enemy'])

        self._init_hitbox((10, 10), pos)

        self.target = None
        self.target_dist = 0
        self.weapon = Weapon(
            sprite_groups, assets, 
            owner=self,
            proj_self_group_key='enemy_projectiles',
            proj_target_group_keys=('player',)
        )

    def update(self, dt):
        if self.target:
            self._follow_target()
        self._move(dt)
        if self.target:
            self.weapon.update(self.look_vec)
            self._attack_target()
        self.animate()

    def animate(self):
        self._flip_image()
        self.weapon.animate()

    def _follow_target(self):
        self_to_target_vec = self.target.pos - self.pos
        self.target_dist = self_to_target_vec.length()
        if not self.target_dist: return
        is_too_far = self.target_dist > self.detection_radius
        if is_too_far:
            self.move_vec *= 0
            self.look_vec.update(copysign(1, self.look_vec.x), 0)
        else:
            normalized = self_to_target_vec.normalize()
            is_too_close = self.target_dist <= self.stop_radius
            self.move_vec = normalized * (not is_too_close)
            self.look_vec = normalized
            
    def _attack_target(self):
        if self.target_dist < self.shoot_radius:
            self.weapon.shoot()