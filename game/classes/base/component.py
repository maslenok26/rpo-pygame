from __future__ import annotations
from abc import ABC, abstractmethod
from typing import final, TYPE_CHECKING

import pygame as pg

from .base_sprite import BaseSprite

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .entity import Entity

class Component(BaseSprite, ABC):
    owner: Entity
    
    def __init__(self, sprite_groups, assets, stats, owner: Entity):
        super().__init__(sprite_groups, assets, owner.rect.center, stats)
        
        self.owner = owner

        self._add_to_groups('entity_components')

    def _sync_with_owner(self):
        self.rect.center = self.owner.rect.center


class ComponentGroup(pg.sprite.Group[Component]):
    def update(self, *args, **kwargs):
        for component in self.sprites():
            if not component.owner.alive():
                component.kill()
            else:
                component.update(*args, **kwargs)