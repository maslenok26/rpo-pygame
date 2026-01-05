from abc import ABC, abstractmethod
from math import copysign

import pygame as pg

from ..settings import SUB_STEP


class Body(pg.sprite.Sprite, ABC):
    def __init__(self, groups):
        super().__init__(groups)

        self.speed = 0

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
            if steps_to_do.x: steps_to_do.x, steps_done.x = self._make_a_step(
                'x', step.x, steps_to_do.x, steps_done.x, collidables
                )
            if steps_to_do.y: steps_to_do.y, steps_done.y = self._make_a_step(
                'y', step.y, steps_to_do.y, steps_done.y, collidables
                )
        self._rem -= steps_done
        self.pos = pg.Vector2(self.rect.center) + self._rem

    @abstractmethod
    def _make_a_step(self, axis, step, steps_to_do, steps_done, collidables):
        ...