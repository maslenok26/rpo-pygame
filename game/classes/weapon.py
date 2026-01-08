import pygame as pg

from .base_sprite import BaseSprite
from .timer import Timer
from .projectile import Projectile
from ..settings import LAYERS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player


class Weapon(BaseSprite):
    def __init__(self, sprite_groups, owner: 'Player'):
        super().__init__(sprite_groups)

        self._layer = LAYERS['WEAPON_FRONT']
        self.add_to_groups('rendering')

        self.orbit_offset = pg.Vector2(3, 4)
        self.muzzle_offset = pg.Vector2(18, -3)
        self.cur_orbit_offset = self.orbit_offset.copy()
        self.cur_muzzle_offset = self.muzzle_offset.copy()

        self.owner = owner
        self.sprite_groups = sprite_groups

        self.orig_image = pg.image.load('assets\\shotgun.png').convert_alpha()
        self.image = self.orig_image
        self.rect = self.image.get_rect(center=self.owner.rect.center)

        self.vector = pg.Vector2(1, 0)

        self.timers = {
            'shoot': Timer(
                duration=0, end_func=None, cooldown=200
            )
        }

    def update(self, player_to_mouse_vec):
        self.rect.center = self.owner.rect.center
        self._rotate(player_to_mouse_vec)
        self._get_input()
        self.timers['shoot'].update()

    def animate(self):
        self._rotate_image()

    def _get_input(self):
        if pg.mouse.get_pressed()[0]: self._shoot()

    def _shoot(self):
        if not self.timers['shoot'].start(): return
        spawn_pos = self.rect.center + self.cur_muzzle_offset
        Projectile(
            self.sprite_groups, *spawn_pos, self.vector
        )

    def _rotate(self, player_to_mouse_vec: pg.Vector2):
        if not player_to_mouse_vec: return
        self.vector = player_to_mouse_vec.normalize()
        angle = self.vector.angle
        self.cur_orbit_offset = self.orbit_offset.copy()
        self.cur_muzzle_offset = self.muzzle_offset.copy()
        if abs(angle) > 90:
            self.cur_orbit_offset.y *= -1
            self.cur_muzzle_offset.y *= -1
        self.cur_orbit_offset.rotate_ip(angle)
        self.cur_muzzle_offset.rotate_ip(angle)
        self.rect.center += self.cur_orbit_offset

    def _rotate_image(self):
        angle = self.vector.angle
        image_to_rotate = self.orig_image
        if self.owner.image_flipped:
            image_to_rotate = pg.transform.flip(
                image_to_rotate, flip_x=False, flip_y=True
                )
        self.image = pg.transform.rotate(image_to_rotate, -angle)
        if angle >= 0: layer = LAYERS['WEAPON_FRONT']
        else: layer = LAYERS['WEAPON_BACK']
        if layer != self._layer:
            self.sprite_groups['rendering'].change_layer(self, layer)
        self.rect = self.image.get_rect(center=self.rect.center)