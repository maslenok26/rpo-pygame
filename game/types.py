from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, NotRequired

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
    face: list[pg.Surface]

class Assets(TypedDict):
    floor: list[pg.Surface]
    walls: WallAssets
    player: list[pg.Surface]
    enemy: list[pg.Surface]
    pistol: list[pg.Surface]
    shotgun: list[pg.Surface]
    projectile: list[pg.Surface]


# ТИПЫ ДЛЯ CONFIG/
class Layers(TypedDict):
    wall_face: int
    enemy: int
    player: int
    projectile: int
    wall_top: int


class FactionRule(TypedDict):
    proj_self_group_key: str
    proj_target_group_keys: tuple[str]


class GeneralStats(TypedDict):
    # entity
    faction: NotRequired[str]
    hp: NotRequired[int]
    # enemy
    detection_radius: NotRequired[int]
    shoot_radius: NotRequired[int]
    stop_radius: NotRequired[int]
    # weapon
    cooldown: NotRequired[int]
    proj_stats: NotRequired[Stats]
    
class PhysicsStats(TypedDict):
    # hitboxsprite
    hitbox_size: NotRequired[tuple[int, int]]
    # body
    speed: NotRequired[float]
    # player
    dash_speed: NotRequired[float]

class RenderStats(TypedDict):
    asset_path: NotRequired[str]

class ComponentsStats(TypedDict):
    timers: NotRequired[dict[str, dict[str, int]]]
    start_weapon_keys: NotRequired[tuple[str]]

class Stats(TypedDict):
    general: NotRequired[GeneralStats]
    physics: NotRequired[PhysicsStats]
    render: NotRequired[RenderStats]
    components: NotRequired[ComponentsStats]

StatsDict = dict[str, Stats]  