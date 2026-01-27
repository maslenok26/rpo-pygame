from __future__ import annotations
from abc import ABC, abstractmethod
from typing import final, TYPE_CHECKING

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

    @final
    def update(self):
        if not self.owner.alive():
            self.kill()
            return
        self._update_logic()

    @abstractmethod
    def _update_logic(self) -> None:
        ...

    def _sync_with_owner(self):
        self.rect.center = self.owner.rect.center