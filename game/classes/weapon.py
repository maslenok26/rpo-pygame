from math import atan2, degrees

import pygame as pg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player


class Weapon(pg.sprite.Sprite):
    def __init__(self, owner: 'Player', groups):
        super().__init__(groups)

        self.owner = owner

        self.orig_image = pg.image.load('assets\\shotgun.png').convert_alpha()
        self.image = self.orig_image
        self.rect = self.image.get_rect(center=self.owner.rect.center)
        self.offset = pg.Vector2(3, 4)

        self.angle = 0

    def update(self):
        self.rect.center = self.owner.rect.center

    def animate(self, mouse_pos, camera_dist):
        self._rotate(mouse_pos, camera_dist)

    def _rotate(self, mouse_pos: pg.Vector2, camera_dist: pg.Vector2):
        self.angle = degrees(atan2(*(mouse_pos - camera_dist)[::-1]))
        image_to_rotate = self.orig_image
        offset = self.offset.copy()
        if self.owner.flipped:
            image_to_rotate = pg.transform.flip(
                image_to_rotate, flip_x=False, flip_y=True
                )
            offset.y *= -1
        offset.rotate_ip(self.angle)
        self.image = pg.transform.rotate(image_to_rotate, -self.angle)
        self.rect = self.image.get_rect(center=self.owner.rect.center + offset)