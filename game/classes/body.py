from abc import ABC, abstractmethod
from math import copysign

import pygame as pg

from .hitbox_sprite import HitboxSprite
from ..settings import SUB_STEP


class Body(HitboxSprite, ABC):
    def __init__(self, sprite_groups):
        super().__init__(sprite_groups)

        self.speed = 0

        self.pos = pg.Vector2(0, 0)
        self.move_vec = pg.Vector2(0, 0)
        self._rem = pg.Vector2(0, 0)

        self.has_shadow = True

    def _move(self, dt, collidables):
        if not self.move_vec: return
        self._rem += self.move_vec * self.speed * dt
        steps_to_do: pg.Vector2 = round(self._rem)
        steps_done = pg.Vector2(0, 0)
        step = pg.Vector2(
            copysign(SUB_STEP, steps_to_do.x),
            copysign(SUB_STEP, steps_to_do.y)
            )
        while steps_to_do:
            if steps_to_do.x:
                step.x, steps_to_do.x, steps_done.x = self._make_a_step(
                    'x', step.x, steps_to_do.x, steps_done.x, collidables
                    )
            if steps_to_do.y: 
                step.y, steps_to_do.y, steps_done.y = self._make_a_step(
                    'y', step.y, steps_to_do.y, steps_done.y, collidables
                    )
        self._rem -= steps_done
        self.pos = self.rect.center + self._rem

    def _make_a_step(self, axis, step, steps_to_do, steps_done, collidables):
        if axis == 'x': self.hitbox.x += step
        elif axis == 'y': self.hitbox.y += step
        collisions = pg.sprite.spritecollide(
            self,
            collidables,
            dokill=False,
            collided=self._check_hitbox_collision
            )
        if not collisions:
            steps_done += step
            steps_to_do -= step
        else:
            if axis == 'x': self.hitbox.x -= step
            elif axis == 'y': self.hitbox.y -= step
            action = self._handle_collision(collisions)
            match action:
                case 'STOP':
                    steps_to_do = 0
                    if axis == 'x': self._rem.x = 0
                    elif axis == 'y': self._rem.y = 0
                case 'BOUNCE':
                    step *= -1
                    steps_to_do *= -1
                    steps_done *= -1
                    if axis == 'x':
                        self.move_vec.x *= -1
                        self._rem.x *= -1
                    elif axis == 'y':
                        self.move_vec.y *= -1
                        self._rem.y *= -1
                case 'DESTROY':
                    steps_to_do = 0
                    self.kill()
        if self.rect:
            self.rect.center = self.hitbox.center
        return step, steps_to_do, steps_done

    @abstractmethod
    def _handle_collision(self, collisions) -> str:
        ...