from abc import ABC, abstractmethod
from math import copysign

import pygame as pg

from ..settings import SUB_STEP


class Body(pg.sprite.Sprite, ABC):
    def __init__(self, sprite_groups):
        super().__init__(sprite_groups)

        self.speed = 0

        self.rect = pg.Rect(0, 0, 0, 0)
        
        self.hitbox = pg.Rect(0, 0, 0, 0)

        self.pos = pg.Vector2(self.rect.center)
        self.vector = pg.Vector2(0, 0)
        self._rem = pg.Vector2(0, 0)

    def _move(self, dt, collidables):
        if not self.vector.length(): return
        self._rem += self.vector * self.speed * dt
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
        is_colliding = pg.sprite.spritecollideany(
            self, collidables, collided=self._check_hitbox_collision
            )
        if not is_colliding:
            steps_done += step
            steps_to_do -= step
        else:
            if axis == 'x': self.hitbox.x -= step
            elif axis == 'y': self.hitbox.y -= step
            action = self._handle_collision()
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
                        self.vector.x *= -1
                        self._rem.x *= -1
                    elif axis == 'y':
                        self.vector.y *= -1
                        self._rem.y *= -1
                case 'DESTROY':
                    steps_to_do = 0
                    self.kill()
        self.rect.center = self.hitbox.center
        return step, steps_to_do, steps_done
    
    def _check_hitbox_collision(
            self, body: 'Body', collidable: pg.sprite.Sprite
            ):
        is_colliding = body.hitbox.colliderect(collidable.rect)
        return is_colliding

    @abstractmethod
    def _handle_collision(self) -> str:
        ...