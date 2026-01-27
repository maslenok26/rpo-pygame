from collections import deque
from random import choice
import pygame as pg

from ..classes import Camera, Wall, Enemy, Player
from ..utils import LevelGenerator, loader
from .. import config as cfg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..types import SpriteGroups, Assets


class GameManager:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.camera = Camera()
        self._init_display()
        self._init_assets()
        self._init_sprite_groups()

    def get_fps(self):
        return cfg.FPS if cfg.FPS_LOCK else 0
    
    def get_mouse_screen_pos(self):
        mouse_pos: pg.Vector2 = (
            (pg.mouse.get_pos() - self.layout.offset) / self.layout.scale
        )
        if cfg.LETTERBOXING:
            mouse_pos.x = pg.math.clamp(mouse_pos.x, 0, cfg.GAME_WIDTH)
            mouse_pos.y = pg.math.clamp(mouse_pos.y, 0, cfg.GAME_HEIGHT)
        game_surf_center = pg.Vector2(cfg.GAME_WIDTH/2, cfg.GAME_HEIGHT/2)
        screen_pos = mouse_pos - game_surf_center
        return screen_pos
    
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
        if not level_map:
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
                y = row_idx * cfg.TILE_SIZE
                x = tile_idx * cfg.TILE_SIZE
                self.static_surf.blit(choice(self._assets['floor']), (x, y))
                spawn_pos = (x + (cfg.TILE_SIZE // 2), y + (cfg.TILE_SIZE // 2))
                context = (self._sprite_groups, self._assets, spawn_pos)
                match tile:
                    case 'W':
                        needs_face = not (row_idx + 1 >= len(level_map))
                        depth = min(wall_depths[(tile_idx, row_idx)], 2)
                        Wall(*context, depth, needs_face)
                    case 'P':
                        player = Player(*context)
                    case 'E':
                        Enemy(*context)
        self._init_player(player)

    def resize(self):
        self.layout.update(self.screen.size)

    def _init_display(self):
        display_flags = pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE
        self.screen = pg.display.set_mode(
            cfg.START_SCREEN_SIZE, flags=display_flags, vsync=1
            )
        self.game_surf = pg.Surface((cfg.GAME_WIDTH, cfg.GAME_HEIGHT))
        self.layout = self._Layout(self.screen.size)
    
    def _init_assets(self):
        self._assets: Assets = {
            'shadows': {},
            'floor': loader.load_folder('assets/grass'),
            'walls': {
                'tops': loader.load_folder('assets/walls/tops'),
                'face': loader.load_asset('assets/walls/wall_face.png')
            },
            'weapons': loader.load_collection('assets/weapons'),
            'player': loader.load_asset('assets/player.png'),
            'skeleton': loader.load_asset('assets/skeleton.png'),
            'projectile': loader.load_asset('assets/projectile.png')
        }
    
    def _init_sprite_groups(self):
        self._sprite_groups: SpriteGroups = {
            'rendering': pg.sprite.LayeredUpdates(),
            'obstacles': pg.sprite.Group(),
            'player': pg.sprite.GroupSingle(),
            'enemies': pg.sprite.Group(),
            'player_projectiles': pg.sprite.Group(),
            'enemy_projectiles': pg.sprite.Group(),
            'entity_components': pg.sprite.Group()
        }

    def _get_wall_depths(self, level_map, level_size):
        width, height = level_size
        depths = {}
        queue = deque()
        for y in range(height):
            for x in range(width):
                if level_map[y][x] == 'W': continue
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
            self.update(screen_size)
        
        def update(self, screen_size):
            screen_width, screen_height = screen_size
            scales = (
                screen_width / cfg.GAME_WIDTH, screen_height / cfg.GAME_HEIGHT
                )
            scale = min(scales) if cfg.LETTERBOXING else max(scales)
            scaled_width = cfg.GAME_WIDTH * scale
            scaled_height = cfg.GAME_HEIGHT * scale
            offset_x = (screen_width - scaled_width) // 2
            offset_y = (screen_height - scaled_height) // 2
            self.scale = scale
            self.offset.update(offset_x, offset_y)
            self.size = (int(scaled_width), int(scaled_height))