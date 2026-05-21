from __future__ import annotations

import pygame as pg

from .base_sprite import BaseSprite
from ... import config as cfg


class UISprite(BaseSprite):
    def __init__(self, sprite_groups, assets, stats):
        
        super().__init__(sprite_groups, assets, stats)

        self.anchor_norm_offset = (
            cfg.ANCHORS_NORM_OFFSETS[self._render['anchor']]
        )
        self._init_rect()
        self._sprite_groups['ui'].add(self)
        
    def _init_rect(self):
        super()._init_rect()
        pos = (
            cfg.GAME_SURF_SIZE.elementwise()
            * self.anchor_norm_offset
            + self._render.get('anchor_offset', (0, 0))
        )
        self.rect.topleft = (
            pos - self._get_image_offset(pg.Vector2(self.image.size))
        )

    def _set_image(self, image):
        old_size = self.image.size
        super()._set_image(image)
        delta = pg.Vector2(self.image.size) - old_size 
        self.rect.center -= self._get_image_offset(delta)

    def _get_image_offset(self, image_delta: pg.Vector2):
        return image_delta.elementwise() * self.anchor_norm_offset