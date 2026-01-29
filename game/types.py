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
    entity_components: pg.sprite.Group[BaseSprite]

    
class WallAssets(TypedDict):
    tops: tuple[pg.Surface]
    face: tuple[pg.Surface]

class Assets(TypedDict):
    shadows: dict[str, tuple[pg.Surface]]
    floor: tuple[pg.Surface]
    walls: WallAssets
    weapons: dict[str, tuple[pg.Surface]]
    player: tuple[pg.Surface]
    enemy: tuple[pg.Surface]
    revolver: tuple[pg.Surface]
    shotgun: tuple[pg.Surface]
    projectile: tuple[pg.Surface]


# ТИПЫ ДЛЯ CONFIG/
class Layers(TypedDict):
    shadow: int
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
    # projectile
    damage: NotRequired[float]
    bounces_left: NotRequired[int]
    # enemy
    detection_radius: NotRequired[int]
    shoot_radius: NotRequired[int]
    stop_radius: NotRequired[int]
    # weapon
    cooldown: NotRequired[int]
    proj_amount: NotRequired[int]
    spread_angle: NotRequired[int]
    proj_stats: NotRequired[StatsLeaf]
    
class PhysicsStats(TypedDict):
    hitbox_size: NotRequired[tuple[int, int]]
    # body
    speed: NotRequired[float]
    # player
    dash_speed: NotRequired[float]
    # projectile
    drag: NotRequired[float]

class RenderStats(TypedDict):
    layer: NotRequired[int]
    asset_path: NotRequired[str]
    # wall
    y_offset: NotRequired[int]

class ComponentsStats(TypedDict):
    timers: NotRequired[dict[str, dict[str, int]]]
    # entity
    start_weapon_keys: NotRequired[tuple[str]]

class StatsLeafBase(TypedDict):
    general: NotRequired[GeneralStats]
    physics: NotRequired[PhysicsStats]
    render: NotRequired[RenderStats]
    components: NotRequired[ComponentsStats]

class StatsLeaf(StatsLeafBase):
    default: StatsLeafBase