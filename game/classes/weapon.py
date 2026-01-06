import pygame as pg

from .timer import Timer
from .projectile import Projectile

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player


class Weapon(pg.sprite.Sprite):
    def __init__(self, sprite_groups, owner: 'Player'):
        super().__init__(sprite_groups['all'])

        self.base_offset = pg.Vector2(3, 4)
        self.base_muzzle_offset = pg.Vector2(18, 0)
        self.offset = self.base_offset.copy()
        self.muzzle_offset = self.base_muzzle_offset.copy()

        self.owner = owner
        self.sprite_groups = sprite_groups

        self.orig_image = pg.image.load('assets\\shotgun.png').convert_alpha()
        self.image = self.orig_image
        self.rect = self.image.get_rect(center=self.owner.rect.center)

        self.vector = pg.Vector2(1, 0)

        self.timers = {
            'shoot': Timer(
                duration=0, end_func=None, cooldown=250
            )
        }

    def update(self):
        self.rect.center = self.owner.rect.center
        self._get_input()
        self.timers['shoot'].update()

    def animate(self, mouse_pos, camera_dist):
        self._rotate(mouse_pos, camera_dist)

    def _get_input(self):
        if pg.mouse.get_pressed()[0]: self._shoot()

    def _shoot(self):
        if not self.timers['shoot'].start(): return
        spawn_pos = self.rect.center + self.muzzle_offset
        Projectile(
            self.sprite_groups, *spawn_pos, self.vector
        )

    def _rotate(self, mouse_pos: pg.Vector2, camera_dist: pg.Vector2):
        mouse_vector = mouse_pos - camera_dist
        self.vector = mouse_vector.normalize()
        angle = mouse_vector.angle
        image_to_rotate = self.orig_image
        self.offset = self.base_offset.copy()
        self.muzzle_offset = self.base_muzzle_offset.copy()
        if self.owner.flipped:
            image_to_rotate = pg.transform.flip(
                image_to_rotate, flip_x=False, flip_y=True
                )
            self.offset.y *= -1
            self.muzzle_offset.y *= -1
        self.offset.rotate_ip(angle)
        self.muzzle_offset.rotate_ip(angle)
        self.image = pg.transform.rotate(image_to_rotate, -angle)
        self.rect = self.image.get_rect(center=self.rect.center + self.offset)