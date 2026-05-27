from __future__ import annotations
from typing import TYPE_CHECKING, Callable

import pygame as pg

from .register_metas import RegisterBaseMeta
from .. import Timer
from ... import config as cfg

if TYPE_CHECKING:
    from ... import types


class BaseSprite(pg.sprite.Sprite, metaclass=RegisterBaseMeta):
    _sprite_groups: types.SpriteGroups
    _register_groups: list[pg.sprite.AbstractGroup]

    _assets: types.Assets

    _stats: types.StatsLeaf
    _general: types.GeneralStats
    _render: types.RenderStats
    _components: types.ComponentsStats

    _orig_image: pg.Surface
    _image_idx: int

    def __init__(self, sprite_groups, assets, stats: types.StatsLeaf):
        super().__init__()

        self._sprite_groups = sprite_groups
        self._register_groups = []

        self._assets = assets

        self._stats = stats
        if cfg.CfgKey.Leaf.GENERAL in self._stats:
            self._general = self._stats['general']
        if cfg.CfgKey.Leaf.COMPONENTS in self._stats:
            self._components = self._stats['components']

        self.rect = pg.Rect()

    def register(self):
        for group in self._register_groups:
            group.add(self)

    def _get_register_groups(self):
        return ()

    def _set_image(self, image: pg.Surface):
        self.image = image
        self.rect.size = self.image.size

    def _setup_render(self):
        self._render = self._stats['render']
        self._asset_path = self._render['asset_path']

    def _init_images(self):
        asset = self._assets[self._asset_path]
        match self._render['asset_type']:
            case cfg.AssetType.SINGLE:
                self._orig_image = asset
            case cfg.AssetType.SEQUENCE:
                self._orig_image = asset[self._image_idx]
            case _:
                raise ValueError('Неизвестный тип ассета')
        self._set_image(self._orig_image)

    def _init_timers(self, **end_funcs):
        self.timers = {
            key: Timer(**self._components['timers'][key], end_func=end_func)
            for key, end_func in end_funcs.items()
        }

    def _update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def _get_shadow_stats(
            self, gen_func: Callable[[pg.Surface], pg.Surface]
            ):
        shadow_asset_path = (
            cfg.SHADOW_PREFIX + cfg.ASSET_PATH_SEP + self._asset_path
        )
        self._assets.setdefault(shadow_asset_path, gen_func(self.image))
        shadow_stats: types.StatsLeaf = {
            'render': {
                'layer': cfg.Layer.SHADOW,
                'asset_path': shadow_asset_path,
                'asset_type': cfg.AssetType.SINGLE,
            }
        }
        return shadow_stats