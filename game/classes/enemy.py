from __future__ import annotations

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
        self.speed = cfg.TILE_SIZE * 3
        self.detection_radius = 120
        self.shoot_radius = 100

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
        if self.target_dist > self.detection_radius:
            self.move_vec *= 0
            self.look_vec.update(1 if self.look_vec.x >= 0 else -1, 0)
            return
        self.move_vec = self_to_target_vec.normalize()
        self.look_vec = self.move_vec.copy()

    def _attack_target(self):
        if self.target_dist < self.shoot_radius:
            self.weapon.shoot()