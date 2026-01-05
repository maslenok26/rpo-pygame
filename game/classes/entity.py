from abc import ABC

import pygame as pg

from .body import Body


class Entity(Body, ABC):
    def _make_a_step(self, axis, step, steps_to_do, steps_done, collidables):
        if axis == 'x':
            self.rect.x += step
        elif axis == 'y':
            self.rect.y += step
        if not pg.sprite.spritecollide(self, collidables, dokill=False):
            steps_done += step
            steps_to_do -= step
        else:
            if axis == 'x':
                self.rect.x -= step
                self._rem.x = 0
            elif axis == 'y':
                self.rect.y -= step
                self._rem.y = 0
            steps_to_do = 0
        return steps_to_do, steps_done