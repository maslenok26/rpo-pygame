from __future__ import annotations
from itertools import chain

import pygame as pg

from . import Body
from .. import config as cfg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import HitboxSprite, Entity
    from ..types import Stats, FactionRule


class Projectile(Body):
    _layer = cfg.LAYERS['projectile']
    target_groups: tuple[pg.sprite.Group]
    collidables: tuple[HitboxSprite]

    def __init__(
            self, sprite_groups, assets, pos, stats: Stats,
            vector: pg.Vector2,
            faction_rule: FactionRule
            ):
        super().__init__(sprite_groups, assets, pos, stats)

        self._add_to_groups('rendering', faction_rule['proj_self_group_key'])

        general = stats['general']
        physics = stats['physics']
        self.damage = general['damage']
        self.bounces_left = general['bounces_left']
        self.drag = physics['drag']
        
        is_inside_obstacle = pg.sprite.spritecollideany(
            self,
            self._sprite_groups['obstacles'], 
            collided=self._check_hitbox_collision
            )
        if is_inside_obstacle:
            self.kill()
            return
        self.target_groups = tuple(
            self._sprite_groups[key]
            for key in faction_rule['proj_target_group_keys']
        )
        self._update_collidables()
        self.move_vec.update(vector)

        self._set_image(pg.transform.rotate(self.image, -vector.angle))
        
        self._init_timers(stats, lifetime=self.kill)
        self.timers['lifetime'].start()
    
    def update(self, dt):
        self._update_collidables()
        self._move(dt)
        self.speed *= 1 - (self.drag * dt)
        self._update_timers()
    
    def _update_collidables(self):
        self.collidables = tuple(
            chain(self._sprite_groups['obstacles'], *self.target_groups)
            )
    
    def _handle_collision(self, collisions):
        for sprite in collisions:
            if any(sprite in group for group in self.target_groups):
                sprite: Entity
                sprite.take_damage(self.damage)
                return 'DESTROY'
        if not self.bounces_left:
            return 'DESTROY'
        self.bounces_left -= 1
        self.image = pg.transform.rotate(self.orig_image, self.move_vec.angle)
        return 'BOUNCE'