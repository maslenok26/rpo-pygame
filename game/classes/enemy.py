from __future__ import annotations

from .entity import Entity
from .weapon import Weapon
from .timer import Timer
from ..settings import LAYERS, TILE_SIZE
from ..utils import scale_image

import pygame as pg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player


class Enemy(Entity):
    def __init__(self, sprite_groups, x, y):
        super().__init__(sprite_groups)

        self._layer = LAYERS['PLAYER'] + 1
        self.add_to_groups('rendering', 'hittables', 'enemies')

        self.hp = 100
        self.damage = 10

        self.speed = TILE_SIZE * 3
        self.detection_radius = 120
        self.shoot_radius = 100

        self.image = scale_image('enemy.png', (14, 14))
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))

        self._init_hitbox(10, 10, self.rect.center)

        self.pos = pg.Vector2(self.rect.center)

        self.target: Player | None = None
        self.target_dist = 0

        self.weapon = Weapon(sprite_groups, owner=self)

    def update(self, dt, collidables):
        if self.target:
            self._follow_target()
        self._move(dt, collidables)
        if self.target and self.weapon:
            self.weapon.update(self.look_vec)
            self._attack_target()
        self.animate()

    def animate(self):
        self._flip_image()
        self.weapon.animate()

    def _follow_target(self):
        self_to_target_vec = self.target.pos - self.pos
        self.target_dist = self_to_target_vec.length()
        if self.target_dist > self.detection_radius:
            self.move_vec *= 0
            self.look_vec.update(1 if self.look_vec.x >= 0 else -1, 0)
            return
        self.move_vec = self_to_target_vec.normalize()
        self.look_vec = self.move_vec.copy()


    def _attack_target(self):
        if self.target_dist < self.shoot_radius:
            self.weapon.shoot()
        
    def _flip_image(self):
        if ((self.look_vec.x < 0 and not self.image_flipped)
            or (self.look_vec.x > 0 and self.image_flipped)):
            self.image = pg.transform.flip(
                self.image, flip_x=True, flip_y=False
                )
            self.image_flipped = not self.image_flipped