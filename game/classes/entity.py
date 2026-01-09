from abc import ABC

import pygame as pg

from .body import Body
from .weapon import Weapon


class Entity(Body, ABC):
    def __init__(self, sprite_groups):
        super().__init__(sprite_groups)
        self.hp = 0
        self.damage = 0
        self.is_dead = False

        self.image_flipped = False

        self.look_vec = pg.Vector2(1, 0)

        self.weapon: Weapon | None = None

    def take_damage(self, amount):
        if self.is_dead: return
        self.hp -= amount
        if self.hp <= 0:
            self.die()
    
    def die(self):
        self.is_dead = True
        self.kill()
        if self.weapon: self.weapon.kill()

    def _handle_collision(self, _):
        return 'STOP'