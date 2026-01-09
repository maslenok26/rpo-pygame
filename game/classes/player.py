from math import copysign

import pygame as pg

from .entity import Entity
from .timer import Timer
from .weapon import Weapon
from ..settings import LAYERS, TILE_SIZE
from ..utils import scale_image


class Player(Entity):
    def __init__(self, sprite_groups, x, y):
        super().__init__(sprite_groups)

        self._layer = LAYERS['PLAYER']
        self.add_to_groups('rendering')

        self.base_speed = TILE_SIZE * 8
        self.dash_speed = self.base_speed * 3
        self.speed = self.base_speed

        self.image = scale_image('player.jpg', (14, 14))
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))

        self._init_hitbox(10, 10, self.rect.center)

        self.pos = pg.Vector2(self.rect.center)

        self.weapon = Weapon(sprite_groups, owner=self)
        self.timers = {'dash': Timer(
            duration=75, end_func=self._stop_dash, cooldown=1000
            )}

    def update_movement(self, dt, collidables):
        self._get_movement_input()
        self._move(dt, collidables)
        self.timers['dash'].update()
    
    def update_actions(self, player_to_mouse_vec: pg.Vector2):
        if player_to_mouse_vec:
            self.look_vec = player_to_mouse_vec.normalize()
        self.weapon.update(self.look_vec)
        self._get_actions_input()

    def animate(self):
        # ...
        self._flip_image()
        if self.weapon: self.weapon.animate()

    def _get_movement_input(self):
        if self.timers['dash'].active: return
        self.move_vec *= 0
        keys = pg.key.get_pressed()
        if keys[pg.K_w]: self.move_vec.y -= 1
        if keys[pg.K_a]: self.move_vec.x -= 1
        if keys[pg.K_s]: self.move_vec.y += 1
        if keys[pg.K_d]: self.move_vec.x += 1
        if self.move_vec:
            self.move_vec.normalize_ip()
            if keys[pg.K_SPACE]: self._start_dash()

    def _get_actions_input(self):
        mouse = pg.mouse.get_pressed()
        if mouse[0]: self.weapon.shoot()
        
    def _start_dash(self):
        if self.timers['dash'].start():
            self.speed = self.dash_speed

    def _stop_dash(self):
        self.speed = self.base_speed

    def _flip_image(self):
        if ((self.look_vec.x < 0 and not self.image_flipped)
            or (self.look_vec.x > 0 and self.image_flipped)):
            self.image = pg.transform.flip(
                self.image, flip_x=True, flip_y=False
                )
            self.image_flipped = not self.image_flipped