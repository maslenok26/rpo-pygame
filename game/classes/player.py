from math import copysign

import pygame as pg

from .entity import Entity
from .timer import Timer
from .weapon import Weapon
from ..settings import TILE_SIZE, SUB_STEP
from ..utils import scale_image


class Player(Entity):
    def __init__(self, x, y, groups):
        super().__init__(groups)

        self.base_speed = TILE_SIZE * 7
        self.dash_speed = self.base_speed * 3
        self.speed = self.base_speed

        self.image = scale_image('vanya.jpg', (14, 14))
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))

        self.pos = pg.Vector2(self.rect.center)
        self.vector = pg.Vector2(0, 0)
        self._rem = pg.Vector2(0, 0)

        self.flipped = False
        self.timers = {'dash': Timer(
            duration=75, end_func=self._stop_dash, cooldown=1000
            )}
        self.weapon = Weapon(self, groups)

    def update(self, dt, collidables):
        self._get_input()
        self._move(dt, collidables)
        self.timers['dash'].update()
        self.weapon.update()

    def animate(self, mouse_pos, camera_dist: pg.Vector2):
        # ...
        self._flip(mouse_pos, camera_dist.x)
        self.weapon.animate(mouse_pos, camera_dist)

    def _get_input(self):
        if self.timers['dash'].active: return
        self.vector *= 0
        keys = pg.key.get_pressed()
        if keys[pg.K_w]: self.vector.y -= 1
        if keys[pg.K_a]: self.vector.x -= 1
        if keys[pg.K_s]: self.vector.y += 1
        if keys[pg.K_d]: self.vector.x += 1
        if self.vector.length():
            self.vector.normalize_ip()
            if keys[pg.K_SPACE]: self._start_dash()
        
    def _start_dash(self):
        if self.timers['dash'].start():
            self.speed = self.dash_speed

    def _stop_dash(self):
        self.speed = self.base_speed

    def _flip(self, mouse_pos: pg.Vector2, camera_dist_x):
        if ((mouse_pos.x < camera_dist_x and not self.flipped)
            or (mouse_pos.x >= camera_dist_x and self.flipped)):
            self.image = pg.transform.flip(
                self.image, flip_x=True, flip_y=False
                )
            self.flipped = not self.flipped