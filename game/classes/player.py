from math import copysign
import pygame as pg

from . import Entity
from .timer import Timer
from .weapon import Weapon
from .. import config as cfg


class Player(Entity):
    _layer = cfg.LAYERS['player']

    def __init__(self, sprite_groups, assets, pos):
        stats = cfg.PLAYER

        super().__init__(sprite_groups, assets, pos, stats)

        self._add_to_groups('rendering', 'player')

        physics = stats['physics']
        self.base_speed = physics['speed']
        self.dash_speed = physics['dash_speed']
        
        self._add_weapons(Weapon, stats['components']['start_weapon_keys'])

        self.timers = {'dash': Timer(
            duration=150, end_func=self._stop_dash, cooldown=500
            )}

    def update_movement(self, dt):
        self._get_movement_input()
        self._move(dt)
        self.timers['dash'].update()
    
    def update_actions(self, self_to_mouse_vec: pg.Vector2):
        if self_to_mouse_vec:
            new_look_vec = self_to_mouse_vec.normalize()
            if new_look_vec.x == 0:
                new_look_vec.x = copysign(cfg.EPSILON, self.look_vec.x)
            self.look_vec.update(new_look_vec)
        for weapon in self.weapons:
            weapon.update()
        self._get_actions_input()

    def animate(self):
        self._flip_image()
        for weapon in self.weapons:
            weapon.animate()

    def _get_movement_input(self):
        if self.timers['dash'].active: return
        self.move_vec *= 0
        keys = pg.key.get_pressed()
        keys_just_pressed = pg.key.get_just_pressed()
        if keys[pg.K_w]: self.move_vec.y -= 1
        if keys[pg.K_a]: self.move_vec.x -= 1
        if keys[pg.K_s]: self.move_vec.y += 1
        if keys[pg.K_d]: self.move_vec.x += 1
        if self.move_vec:
            self.move_vec.normalize_ip()
            if keys_just_pressed[pg.K_SPACE]: self._start_dash()

    def _get_actions_input(self):
        mouse = pg.mouse.get_just_pressed()
        if mouse[0]: self.weapon.shoot()
        if mouse[2]: self._switch_weapons()
        
    def _start_dash(self):
        if self.timers['dash'].start():
            self.speed = self.dash_speed

    def _stop_dash(self):
        self.speed = self.base_speed

    def _switch_weapons(self):
        self.weapon.unequip()
        self.weapon = self.weapons[abs(self.weapons.index(self.weapon)-1)]
        self.weapon.equip()