from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from .classes.base_sprite import BaseSprite


class SpriteGroups(TypedDict):
    rendering: pg.sprite.LayeredUpdates[BaseSprite]
    collidables: pg.sprite.Group[BaseSprite]
    enemies: pg.sprite.Group[BaseSprite]
    projectiles: pg.sprite.Group[BaseSprite]
    hittables: pg.sprite.Group[BaseSprite]