from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from .classes import BaseSprite, HitboxSprite, Player, Enemy, Projectile


# ТИПЫ ДЛЯ MANAGER.PY
class SpriteGroups(TypedDict):
    rendering: pg.sprite.LayeredUpdates[BaseSprite]
    obstacles: pg.sprite.Group[HitboxSprite]
    player: pg.sprite.GroupSingle[Player]
    enemies: pg.sprite.Group[Enemy]
    player_projectiles: pg.sprite.Group[Projectile]
    enemy_projectiles: pg.sprite.Group[Projectile]


class WallAssets(TypedDict):
    tops: list[pg.Surface]
    face: pg.Surface


class Assets(TypedDict):
    floor: list[pg.Surface]
    walls: WallAssets
    player: pg.Surface
    enemy: pg.Surface
    pistol: pg.Surface
    shotgun: pg.Surface
    projectile: pg.Surface


# ТИПЫ ДЛЯ CONFIG.PY
class Layers(TypedDict):
    WALL_FACE: int
    ENEMY: int
    PLAYER: int
    PROJECTILE: int
    WALL_TOP: int


class CombatRule(TypedDict):
    proj_self_group_key: str
    proj_target_group_keys: tuple[str]

CombatRules = dict[str, CombatRule] 


class StaticProjectileStats(TypedDict):
    hitbox_size: tuple[int, int]

ProjectileStats = dict[str, StaticProjectileStats]


class DynamicProjectileStats(TypedDict):
    speed: float
    damage: float
    lifetime: int


class SingleWeaponStats(TypedDict):
    cooldown: int
    orbit_offset: tuple[int, int]
    muzzle_offset: tuple[int, int]
    holstered_offset: tuple[int, int]
    proj_type_key: str
    proj_stats: DynamicProjectileStats

WeaponStats = dict[str, SingleWeaponStats]