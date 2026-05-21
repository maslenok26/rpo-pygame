from __future__ import annotations
from abc import ABC

import pygame as pg

from .world_sprite import WorldSprite

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .entity import Entity

class Component(WorldSprite, ABC):
    owner: Entity
    
    def __init__(self, sprite_groups, assets, stats, owner: Entity):
        self.owner = owner

        super().__init__(sprite_groups, assets, self.owner.rect.center, stats)

        self._sprite_groups['entity_components'].add(self)

    def _sync_with_owner(self):
        self.rect.center = self.owner.rect.center


class ComponentGroup(pg.sprite.Group[Component]):
    def update(self, *args, **kwargs):
        for component in self.sprites():
            if not component.owner.alive():
                component.kill()
            else:
                component.update(*args, **kwargs)