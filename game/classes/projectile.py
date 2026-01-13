from __future__ import annotations
from itertools import chain

import pygame as pg

from . import Body
from .timer import Timer
from .. import config as cfg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import HitboxSprite, Entity


class Projectile(Body):
    target_groups: tuple[pg.sprite.Group]
    collidables: tuple[HitboxSprite]

    def __init__(self, sprite_groups, assets, pos,
                 vector: pg.Vector2, self_group_key, target_group_keys):
        super().__init__(sprite_groups, assets, pos)

        self._layer = cfg.LAYERS['PROJECTILE']
        self.add_to_groups('rendering', self_group_key)

        self.speed = 180
        self.damage = 20

        self.orig_image = self.assets['projectile']
        self.set_image(pg.transform.rotate(self.orig_image, -vector.angle))
        
        self._init_hitbox((8, 6), self.rect.center)
        is_colliding = pg.sprite.spritecollideany(
            self,
            self.sprite_groups['obstacles'], 
            collided=self._check_hitbox_collision
            )
        if is_colliding:
            self.kill()
            return
        self.target_groups = tuple(
            self.sprite_groups[key] for key in target_group_keys
        )
        self._update_collidables()

        self.move_vec = vector
        
        self.timers = {
            'lifetime': Timer(
                duration=3000, end_func=self.kill, cooldown=0
            )
        }
        self.timers['lifetime'].start()
    
    def update(self, dt):
        self._update_collidables()
        self._move(dt)
        self.timers['lifetime'].update()
    
    def _update_collidables(self):
        self.collidables = tuple(
            chain(self.sprite_groups['obstacles'], *self.target_groups)
            )
    
    def _handle_collision(self, collisions):
        for sprite in collisions:
            if any(sprite in group for group in self.target_groups):
                sprite: Entity
                sprite.take_damage(self.damage)
                return 'DESTROY'
        self.image = pg.transform.rotate(self.orig_image, self.move_vec.angle)
        return 'BOUNCE'