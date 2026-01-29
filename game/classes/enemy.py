from __future__ import annotations
from math import copysign

from . import Entity
from .weapon import Weapon
from .. import config as cfg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player


class Enemy(Entity):
    target: Player | None

    def __init__(self, sprite_groups, assets, pos):
        stats = cfg.ENEMIES['skeleton']

        super().__init__(sprite_groups, assets, pos, stats, WeaponClass=Weapon)

        self._add_to_groups('enemies')

        general = stats['general']
        
        self.detection_radius = general['detection_radius']
        self.shoot_radius = general['shoot_radius']
        self.stop_radius = general['stop_radius']

        self._init_timers(stats, shoot=None)

        self.target = None
        self.target_dist = 0

    def update(self, dt):
        if self.target:
            self._follow_target()
        self._move(dt)
        if self.target:
            self.weapon.aim()
            self._attack_target()
        self._update_timers()
        self._animate()

    def _animate(self):
        self._flip_image()

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
            self.look_vec.update(normalized)
            
    def _attack_target(self):
        if (self.target_dist < self.shoot_radius and
            self.timers['shoot'].start()):
            self.weapon.shoot()