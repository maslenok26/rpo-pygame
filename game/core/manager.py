from collections import deque
from random import choice
import pygame as pg

from . import asset_loader
from .level_gen import LevelGenerator
from ..classes import Camera, Wall, Enemy, Player, ComponentGroup
from .. import config as cfg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..types import SpriteGroups


class GameManager:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.camera = Camera()
        self._init_display()
        self._init_assets()
        self._init_sprite_groups()

    def get_fps(self):
        return cfg.FPS * cfg.FPS_LOCK
    
    def get_mouse_screen_pos(self):
        mouse_pos: pg.Vector2 = (
            (pg.mouse.get_pos() - self.layout.offset) / self.layout.scale
        )
        if cfg.LETTERBOXING:
            mouse_pos.update(
                pg.math.clamp(mouse_pos.x, 0, cfg.GAME_SURF_SIZE.x),
                pg.math.clamp(mouse_pos.y, 0, cfg.GAME_SURF_SIZE.y)
            )
        return mouse_pos - cfg.GAME_SURF_CENTER
    
    def update(self, dt):
        if not self.player.alive(): return
        self.player.update_movement(dt)
        self._sprite_groups['enemies'].update(dt)
        self._sprite_groups['player_projectiles'].update(dt)
        self._sprite_groups['enemy_projectiles'].update(dt)
        mouse_screen_pos = self.get_mouse_screen_pos()
        self.camera.update(dt, self.player, mouse_screen_pos)
        player_to_mouse_vec = mouse_screen_pos - self.camera.target_dist
        self.player.update_actions(player_to_mouse_vec)
        self.player.animate()
        self._sprite_groups['entity_components'].update()

    def draw(self):
        self.game_surf.fill(cfg.BG_WALL_COLOR)
        self.screen.fill((0, 0, 0))
        camera_offset = self.camera.get_offset()
        self.game_surf.blit(self.static_surf, camera_offset)
        for sprite in self._sprite_groups['rendering']:
            self.game_surf.blit(sprite.image, sprite.rect.move(camera_offset))
        scaled_game_surf = pg.transform.scale(
            self.game_surf, self.layout.size
            )
        self.screen.blit(scaled_game_surf, self.layout.offset)

    def init_level(self, level_map: list[str]=None):
        if level_map is None:
            level_map = LevelGenerator(
                width=40, height=40, floor_percent=0.3,
                walkers_amount=1, walkers_min=1, walkers_max=2,
                spawn_chance=0.05, death_chance=0.02, turn_chance=0.2,
                enemy_amount=15
                ).get_level()
        width = len(level_map[0])
        height = len(level_map)
        wall_depths = self._get_wall_depths(level_map, (width, height))
        self.static_surf = pg.Surface(
            ((width-1)*cfg.TILE_SIZE, (height-1)*cfg.TILE_SIZE)
            )
        sprite_group: pg.sprite.AbstractGroup
        for sprite_group in self._sprite_groups.values():
            sprite_group.empty()
        for row_idx, row in enumerate(level_map):
            for tile_idx, tile in enumerate(row):
                topleft = tuple(idx * cfg.TILE_SIZE for idx in (tile_idx, row_idx))
                # для пола указывается top-left коорда
                self.static_surf.blit(choice(self._assets['grass']), topleft)
                # для тел указывается коорда центра, все выровняется после установки картинки
                spawn_pos = tuple(axis + cfg.TILE_SIZE // 2 for axis in topleft)
                context = (self._sprite_groups, self._assets, spawn_pos)
                match tile:
                    case cfg.GameObject.FLOOR: pass
                    case cfg.GameObject.WALL:
                        needs_face = row_idx + 1 < len(level_map)
                        depth = min(wall_depths[(tile_idx, row_idx)], 2)
                        Wall(*context, depth, needs_face)
                    case cfg.GameObject.PLAYER: player = Player(*context)
                    case cfg.GameObject.ENEMY: Enemy(*context)
                    case _: raise ValueError(
                            f'Неизвестное обозначение объекта на карте'
                            )
        self._init_player(player)

    def resize(self):
        self.layout.update(self.screen.size)

    def _init_display(self):
        display_flags = pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE
        self.screen = pg.display.set_mode(
            cfg.START_SCREEN_SIZE, flags=display_flags, vsync=1
            )
        self.game_surf = pg.Surface(cfg.GAME_SURF_SIZE)
        self.layout = self._Layout(self.screen.size)
    
    def _init_assets(self):
        self._assets = asset_loader.load_assets('assets')
    
    def _init_sprite_groups(self):
        self._sprite_groups: SpriteGroups = {
            'rendering': pg.sprite.LayeredUpdates(),
            'obstacles': pg.sprite.Group(),
            'player': pg.sprite.GroupSingle(),
            'enemies': pg.sprite.Group(),
            'player_projectiles': pg.sprite.Group(),
            'enemy_projectiles': pg.sprite.Group(),
            'entity_components': ComponentGroup()
        }

    def _get_wall_depths(self, level_map, level_size):
        width, height = level_size
        depths = {}
        queue = deque()
        for y in range(height):
            for x in range(width):
                if level_map[y][x] is cfg.GameObject.WALL:
                    continue
                depths[(x, y)] = -1
                queue.append((x, y))
        while queue:
            x, y = queue.popleft()
            depth = depths[(x, y)]
            for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                cur_x = x + dx
                cur_y = y + dy
                if (not (0 <= cur_x < width and 0 <= cur_y < height)
                    or (cur_x, cur_y) in depths):
                    continue
                cur_depth = depth + 1
                depths[(cur_x, cur_y)] = cur_depth
                queue.append((cur_x, cur_y))
        return depths

    def _init_player(self, player: Player):
        self.player = player
        for enemy in self._sprite_groups['enemies']:
            enemy.target = player


    class _Layout:
        def __init__(self, screen_size):
            self.offset = pg.Vector2()
            self.size = pg.Vector2()
            self.update(screen_size)
        
        def update(self, screen_size: tuple[int, int]):
            scales = tuple(
                size1 / size2
                for size1, size2 in zip(screen_size, cfg.GAME_SURF_SIZE)
                )
            scale = min(scales) if cfg.LETTERBOXING else max(scales)
            scaled_size = cfg.GAME_SURF_SIZE * scale
            offsets = (screen_size - scaled_size) // 2 
            self.scale = scale
            self.offset.update(*offsets)
            self.size.update(*(int(axis) for axis in scaled_size))