from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from .classes import BaseSprite, HitboxSprite, Player, Enemy, Projectile


class Layers(TypedDict):
    WALL_FACE: int
    ENEMY: int
    PLAYER: int
    PROJECTILE: int
    WALL_TOP: int
    

class SpriteGroups(TypedDict):
    rendering: pg.sprite.LayeredUpdates[BaseSprite]
    obstacles: pg.sprite.Group[HitboxSprite]
    player: pg.sprite.GroupSingle[Player]
    enemies: pg.sprite.Group[Enemy]
    player_projectiles: pg.sprite.Group[Projectile]
    enemy_projectiles: pg.sprite.Group[Projectile]


class Assets(TypedDict):
    floor: tuple[pg.Surface]
    wall_top: pg.Surface
    wall_face: pg.Surface
    player: pg.Surface
    enemy: pg.Surface
    shotgun: pg.Surface
    projectile: pg.Surface