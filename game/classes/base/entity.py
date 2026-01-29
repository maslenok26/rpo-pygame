from __future__ import annotations
from abc import ABC
from random import choice

import pygame as pg

from .component import Component
from .body import Body
from ...utils import generate_entity_shadow

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..weapon import Weapon
    from ...types import StatsLeaf


class Entity(Body, ABC):
    image_flipped = False
    weapons: list[Weapon]
    weapon: Weapon

    def __init__(
            self, sprite_groups, assets, pos, stats: StatsLeaf,
            WeaponClass: type[Weapon]
            ):
        super().__init__(sprite_groups, assets, pos, stats)
        
        general = stats['general']
        self.faction = general['faction']
        self.hp = general['hp']

        self.collidables = self._sprite_groups['obstacles']
        self.look_vec = pg.Vector2(choice(((1, 0), (-1, 0))))

        shadow_stats = self._get_shadow_stats(generate_entity_shadow)
        self.shadow = DynamicShadow(
            sprite_groups, assets, shadow_stats, owner=self
            )

        self._add_weapons(
            WeaponClass, stats['components']['start_weapon_keys']
            )
        
    def _handle_collision(self, _):
        return 'STOP'

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.die()
    
    def die(self):
        self.kill()
    
    def _add_weapons(self, WeaponClass: type[Weapon], type_keys):
        self.weapons = []
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
        
    def _flip_image(self):
        should_flip = self.look_vec.x < 0
        if should_flip != self.image_flipped:
            self.image = pg.transform.flip(
                self.image, flip_x=True, flip_y=False
                )
            self.image_flipped = not self.image_flipped


class DynamicShadow(Component):
    def __init__(self, sprite_groups, assets, stats, owner):
        super().__init__(sprite_groups, assets, stats, owner)

        self.offset = self.rect.height * 2.5

    def update(self):
        self._sync_with_owner()
        self.rect.centery += self.offset