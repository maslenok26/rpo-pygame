from math import copysign

import pygame as pg

from .entity import Entity
from .timer import Timer
from .weapon import Weapon
from ..settings import TILE_SIZE, SUB_STEP
from ..utils import scale_image


class Player(Entity):
    def __init__(self, sprite_groups, x, y):
        super().__init__(sprite_groups['all'])

        self.base_speed = TILE_SIZE * 7
        self.dash_speed = self.base_speed * 3
        self.speed = self.base_speed

        self.image = scale_image('vanya.jpg', (14, 14))
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))

        self.hitbox = pg.Rect(0, 0, 8, 8)
        self.hitbox.center = self.rect.center

        self.pos = pg.Vector2(self.rect.center)
        self.vector = pg.Vector2(0, 0)
        self._rem = pg.Vector2(0, 0)

        self.flipped = False
        self.timers = {'dash': Timer(
            duration=75, end_func=self._stop_dash, cooldown=1000
            )}
        self.weapon = Weapon(sprite_groups, self)

    def update_movement(self, dt, collidables):
        self._get_input()
        self._move(dt, collidables)
        self.timers['dash'].update()
    
    def update_actions(self, player_to_mouse_vec):
        self.weapon.update(player_to_mouse_vec)

    def animate(self, player_to_mouse_vec_x):
        # ...
        self._flip(player_to_mouse_vec_x)
        self.weapon.animate()

    def _get_input(self):
        if self.timers['dash'].active: return
        self.vector *= 0
        keys = pg.key.get_pressed()
        if keys[pg.K_w]: self.vector.y -= 1
        if keys[pg.K_a]: self.vector.x -= 1
        if keys[pg.K_s]: self.vector.y += 1
        if keys[pg.K_d]: self.vector.x += 1
        if self.vector:
            self.vector.normalize_ip()
            if keys[pg.K_SPACE]: self._start_dash()
        
    def _start_dash(self):
        if self.timers['dash'].start():
            self.speed = self.dash_speed

    def _stop_dash(self):
        self.speed = self.base_speed

    def _flip(self, player_to_mouse_vec_x: pg.Vector2):
        if ((player_to_mouse_vec_x < 0 and not self.flipped)
            or (player_to_mouse_vec_x >= 0 and self.flipped)):
            self.image = pg.transform.flip(
                self.image, flip_x=True, flip_y=False
                )
            self.flipped = not self.flipped