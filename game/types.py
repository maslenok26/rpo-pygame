from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, NotRequired, Literal

import pygame as pg

if TYPE_CHECKING:
    from .classes import BaseSprite, HitboxSprite, Player, Enemy, Projectile
    from . import config as cfg


# ТИПЫ ДЛЯ MANAGER.PY
class SpriteGroups(TypedDict):
    rendering: pg.sprite.LayeredUpdates[BaseSprite]
    obstacles: pg.sprite.Group[HitboxSprite]
    player: pg.sprite.GroupSingle[Player]
    enemies: pg.sprite.Group[Enemy]
    player_projectiles: pg.sprite.Group[Projectile]
    enemy_projectiles: pg.sprite.Group[Projectile]
    entity_components: pg.sprite.Group[BaseSprite]


# ТИПЫ ДЛЯ CONFIG/
class FactionRule(TypedDict):
    proj_self_group_key: str
    proj_target_group_keys: tuple[str, ...]


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
    asset_type: NotRequired[cfg.AssetType]
    # wall
    y_offset: NotRequired[int]

class ComponentsStats(TypedDict):
    timers: NotRequired[dict[str, TimerStats]]
    # entity
    start_weapon_keys: NotRequired[tuple[str, ...]]

class TimerStats(TypedDict):
    duration: NotRequired[int]
    cooldown: NotRequired[int]

class StatsLeaf(TypedDict):
    general: NotRequired[GeneralStats]
    physics: NotRequired[PhysicsStats]
    render: NotRequired[RenderStats]
    components: NotRequired[ComponentsStats]

type TreeContent = dict[str, StatsLeaf | cfg.Tree]
type MergedTree = dict[str, StatsLeaf | MergedTree]