from __future__ import annotations
from abc import ABC

import pygame as pg

from .base_sprite import BaseSprite
from .body import Body
from ...utils import generate_entity_shadow
from ... import config as cfg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..weapon import Weapon
    from ...types import Stats


class Entity(Body, ABC):
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

        shadow_stats = self._get_shadow_stats(generate_entity_shadow)
        self.shadow = DynamicShadow(
            sprite_groups, assets, shadow_stats, owner=self
            )

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
        self.shadow.kill()
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


class DynamicShadow(BaseSprite):
    _layer = cfg.LAYERS['shadow']

    def __init__(self, sprite_groups, assets, stats, owner: Entity):
        super().__init__(sprite_groups, assets, owner.rect.center, stats)

        self._add_to_groups('rendering')

        self.owner = owner

        self.offset = self.rect.height * 2.5

    def update(self):
        self.rect.center = (
            self.owner.rect.centerx,
            self.owner.rect.centery + self.offset
        )