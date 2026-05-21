from __future__ import annotations

from .base_sprite import BaseSprite
from ... import config as cfg


class WorldSprite(BaseSprite):
    def __init__(self, sprite_groups, assets, pos, stats):
        super().__init__(sprite_groups, assets, stats)

        self._init_rect(pos)
        self._sprite_groups['world_render'].add(self)

    def _setup_render(self):
        if cfg.CfgKey.Leaf.RENDER not in self._stats:
            return
        super()._setup_render()

    def _init_rect(self, pos):
        super()._init_rect()
        self.rect.center = pos

    def _set_image(self, image):
        center = self.rect.center
        super()._set_image(image)
        self.rect.center = center