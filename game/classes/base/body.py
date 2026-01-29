from __future__ import annotations
from abc import ABC, abstractmethod
from math import copysign

import pygame as pg

from .hitbox_sprite import HitboxSprite
from ... import config as cfg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...types import StatsLeaf


class Body(HitboxSprite, ABC):
    collidables: pg.sprite.Group[HitboxSprite] | tuple[HitboxSprite]
    
    def __init__(self, sprite_groups, assets, pos, stats: StatsLeaf):
        super().__init__(sprite_groups, assets, pos, stats)

        self.speed = stats['physics']['speed']
        
        self.pos = pg.Vector2(*pos)
        self.move_vec = pg.Vector2()
        self._remainder = pg.Vector2()

    def _move(self, dt):
        if not self.move_vec: return
        self._remainder += self.move_vec * self.speed * dt
        steps_to_do: pg.Vector2 = round(self._remainder)
        while steps_to_do:
            if steps_to_do.x:
                self._make_a_step(steps_to_do, axis_idx=0)
            if steps_to_do.y: 
                self._make_a_step(steps_to_do, axis_idx=1)
        self.pos = self.rect.center + self._remainder

    def _make_a_step(self, steps_to_do: pg.Vector2, axis_idx):
        step = copysign(
            min(abs(steps_to_do[axis_idx]), cfg.SUB_STEP_LIMIT),
            steps_to_do[axis_idx]
            )
        self.hitbox[axis_idx] += step
        collisions = pg.sprite.spritecollide(
            self,
            self.collidables,
            dokill=False,
            collided=self._check_hitbox_collision
            )
        if not collisions:
            steps_to_do[axis_idx] -= step
            self._remainder[axis_idx] -= step
        else:
            collidable = collisions[0]
            overlap = copysign(
                self.hitbox.clip(collidable.hitbox)[2+axis_idx], step
            )
            self.hitbox[axis_idx] -= overlap
            action = self._handle_collision(collisions)
            match action:
                case 'STOP':
                    steps_to_do[axis_idx] = 0
                    self._remainder[axis_idx] = 0
                case 'BOUNCE':
                    self.move_vec[axis_idx] *= -1
                    steps_to_do[axis_idx] *= -1
                    self._remainder[axis_idx] *= -1
                    self.hitbox[axis_idx] -= overlap
                case 'DESTROY':
                    steps_to_do *= 0
                    self.kill()
        self.rect.center = self.hitbox.center

    @abstractmethod
    def _handle_collision(self, collisions) -> str:
        ...