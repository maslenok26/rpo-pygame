from __future__ import annotations
from abc import ABC

import pygame as pg

from .body import Body

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..weapon import Weapon
    from ...types import Stats


class Entity(Body, ABC):
    has_shadow = True
    image_flipped = False
    weapons: list[Weapon]
    weapon: Weapon = None

    def __init__(self, sprite_groups, assets, pos, stats: Stats):
        super().__init__(sprite_groups, assets, pos, stats)
        
        general = stats['general']
        self.faction = general['faction']
        self.hp = general['hp']

        self.collidables = self._sprite_groups['obstacles']
        self.look_vec = pg.Vector2()

        self.weapons = []

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.die()
    
    def die(self):
        self.kill()

    def kill(self):
        for weapon in self.weapons:
            weapon.kill()
        super().kill()

    def _handle_collision(self, _):
        return 'STOP'

    def _flip_image(self):
        should_flip = self.look_vec.x < 0
        if should_flip != self.image_flipped:
            self.image = pg.transform.flip(
                self.image, flip_x=True, flip_y=False
                )
            self.image_flipped = not self.image_flipped

    def _add_weapons(self, WeaponClass: type[Weapon], type_keys):
        for type_key in type_keys:
            weapon = WeaponClass(
                self._sprite_groups, self._assets,
                type_key, owner=self
                )
            if not self.weapons:
                self.weapon = weapon
            else:
                weapon.unequip()
            self.weapons.append(weapon)