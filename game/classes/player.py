import pygame as pg

from . import Entity
from .timer import Timer
from .weapon import Weapon
from .. import config as cfg


class Player(Entity):
    def __init__(self, sprite_groups, assets, pos):
        super().__init__(sprite_groups, assets, pos)

        self._layer = cfg.LAYERS['PLAYER']
        self.add_to_groups('rendering', 'player')

        self.base_speed = 135
        self.dash_speed = self.base_speed * 3
        self.hp = float('inf')
        self.speed = self.base_speed

        self.set_image(self.assets['player'])

        self._init_hitbox((10, 10), self.rect.center)

        self.timers = {'dash': Timer(
            duration=75, end_func=self._stop_dash, cooldown=1000
            )}
        
        self.weapon = Weapon(
            sprite_groups, assets, 
            owner=self,
            proj_self_group_key='player_projectiles',
            proj_target_group_keys=('enemies', 'player')
        )

    def update_movement(self, dt):
        self._get_movement_input()
        self._move(dt)
        self.timers['dash'].update()
    
    def update_actions(self, player_to_mouse_vec: pg.Vector2):
        if player_to_mouse_vec:
            self.look_vec = player_to_mouse_vec.normalize()
        self.weapon.update(self.look_vec)
        self._get_actions_input()

    def animate(self):
        self._flip_image()
        self.weapon.animate()

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