from __future__ import annotations

from .base_sprite import BaseSprite
from ... import config as cfg


class WorldSprite(BaseSprite):
    _LAYER_KNOWN = True

    def __init__(self, sprite_groups, assets, pos, stats):
        super().__init__(sprite_groups, assets, stats)

        self.rect.center = pos

        if cfg.CfgKey.Leaf.RENDER not in self._stats:
            return
        
        self._register_groups.append(self._sprite_groups['world_render'])

        self._setup_render()
        self._init_images()
        if not self._LAYER_KNOWN: return
        self.layer = self._render['layer']

    def _set_image(self, image):
        center = self.rect.center
        super()._set_image(image)
        self.rect.center = center