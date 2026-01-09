from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from .classes.base_sprite import BaseSprite
    from .classes.hitbox_sprite import HitboxSprite
    from .classes.enemy import Enemy
    from .classes.projectile import Projectile


class SpriteGroups(TypedDict):
    rendering: pg.sprite.LayeredUpdates[BaseSprite]
    collidables: pg.sprite.Group[HitboxSprite]
    enemies: pg.sprite.Group[Enemy]
    projectiles: pg.sprite.Group[Projectile]
    hittables: pg.sprite.Group[HitboxSprite]