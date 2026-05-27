from __future__ import annotations

import pygame as pg

from .base_sprite import BaseSprite
from ... import config as cfg


class UISprite(BaseSprite):
    def __init__(self, sprite_groups, assets, stats):
        super().__init__(sprite_groups, assets, stats)

        self._register_groups.append(self._sprite_groups['ui'])

        self._setup_render()
        self.anchor_norm_offset = (
            cfg.ANCHORS_NORM_OFFSETS[self._render['anchor']]
        )
        self.rect.topleft = (
            cfg.GAME_SURF_SIZE.elementwise() * self.anchor_norm_offset
            + self._render.get('anchor_offset', (0, 0))
        )
        self._init_images()

    def _set_image(self, image):
        old_size = self.image.size if self.image is not None else (0, 0)
        super()._set_image(image)
        delta = pg.Vector2(self.image.size) - old_size 
        self.rect.center -= self._get_image_offset(delta)

    def _get_image_offset(self, image_delta: pg.Vector2):
        return image_delta.elementwise() * self.anchor_norm_offset