from __future__ import annotations
from itertools import chain

import pygame as pg

from . import Body
from .timer import Timer
from .. import config as cfg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import HitboxSprite, Entity
    from ..types import DynamicProjectileStats


class Projectile(Body):
    target_groups: tuple[pg.sprite.Group]
    collidables: tuple[HitboxSprite]

    def __init__(
            self, sprite_groups, assets, pos,
            type_key,
            vector: pg.Vector2,
            self_group_key, target_group_keys,
            dynamic_stats: DynamicProjectileStats
            ):
        super().__init__(sprite_groups, assets, pos)

        self._layer = cfg.LAYERS['PROJECTILE']
        self.add_to_groups('rendering', self_group_key)

        static_stats = cfg.PROJECTILE_STATS[type_key]

        self.speed = dynamic_stats['speed']
        self.damage = dynamic_stats['damage']

        self.orig_image = self._assets[type_key]
        self.set_image(pg.transform.rotate(self.orig_image, -vector.angle))
        
        hb_width, hb_height = static_stats['hitbox_size']
        if abs(vector.y) > abs(vector.x):
            hb_width, hb_height = hb_height, hb_width
        self._init_hitbox((hb_width, hb_height), self.rect.center)
        is_colliding = pg.sprite.spritecollideany(
            self,
            self._sprite_groups['obstacles'], 
            collided=self._check_hitbox_collision
            )
        if is_colliding:
            self.kill()
            return
        self.target_groups = tuple(
            self._sprite_groups[key] for key in target_group_keys
        )
        self._update_collidables()

        self.move_vec = vector.copy()
        
        self.timers = {
            'lifetime': Timer(
                duration=dynamic_stats['lifetime'], end_func=self.kill
            )
        }
        self.timers['lifetime'].start()
    
    def update(self, dt):
        self._update_collidables()
        self._move(dt)
        self.timers['lifetime'].update()
    
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
        self.image = pg.transform.rotate(self.orig_image, self.move_vec.angle)
        return 'BOUNCE'