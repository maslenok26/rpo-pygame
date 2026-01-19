from os import listdir
from random import choice

import pygame as pg

from ..classes import Camera, Wall, Enemy, Player
from ..utils import LevelGenerator
from .. import config as cfg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..types import SpriteGroups, Assets


class GameManager:
    def __init__(self):
        self._init_display()
        self._init_assets()
        self._init_clock()
        self._init_sprite_groups()
        self._init_camera()

    def get_fps(self):
        return cfg.FPS if cfg.FPS_LOCK else 0
    
    def get_mouse_screen_pos(self):
        mouse_pos: pg.Vector2 = (
            (pg.mouse.get_pos() - self.layout.offset) / self.layout.scale
        )
        if cfg.LETTERBOXING:
            mouse_pos.x = pg.math.clamp(mouse_pos.x, 0, cfg.GAME_WIDTH)
            mouse_pos.y = pg.math.clamp(mouse_pos.y, 0, cfg.GAME_HEIGHT)
        game_surf_center = pg.Vector2(cfg.GAME_WIDTH / 2, cfg.GAME_HEIGHT / 2)
        screen_pos = mouse_pos - game_surf_center
        return screen_pos
    
    def update(self, dt):
        if self.player.is_dead: return
        self.player.update_movement(dt)
        self.sprite_groups['enemies'].update(dt)
        self.sprite_groups['player_projectiles'].update(dt)
        self.sprite_groups['enemy_projectiles'].update(dt)
        mouse_screen_pos = self.get_mouse_screen_pos()
        self.camera.update(dt, self.player, mouse_screen_pos)
        player_to_mouse_vec = mouse_screen_pos - self.camera.target_dist
        self.player.update_actions(player_to_mouse_vec)
        self.player.animate()

    def draw(self):
        self.game_surf.fill((0, 0, 0))
        self.screen.fill((0, 0, 0))
        camera_offset = self.camera.get_offset()
        self.game_surf.blit(self.static_surf, camera_offset)
        for sprite in self.sprite_groups['rendering']:
            self.game_surf.blit(sprite.image, sprite.rect.move(camera_offset))
        scaled_game_surf = pg.transform.scale(
            self.game_surf, self.layout.size
            )
        self.screen.blit(scaled_game_surf, self.layout.offset)

    def init_level(self, level_map: list[str]=None):
        if not level_map:
            level_map = LevelGenerator(
                40, 40, floor_percent=0.3,
                walkers_amount=1, walkers_min=1, walkers_max=2,
                spawn_chance=0.05, death_chance=0.02, turn_chance=0.3,
                enemy_amount=15
                ).get_level()
        self.static_surf = pg.Surface(
            (len(level_map[0])*cfg.TILE_SIZE, len(level_map)*cfg.TILE_SIZE)
            )
        sprite_group: pg.sprite.AbstractGroup
        for sprite_group in self.sprite_groups.values():
            sprite_group.empty()
        dynamic_objects = {'W': Wall, 'P': Player, 'E': Enemy}
        for row_idx, row in enumerate(level_map):
            for tile_idx, tile in enumerate(row):
                y = row_idx * cfg.TILE_SIZE
                x = tile_idx * cfg.TILE_SIZE
                self.static_surf.blit(choice(self.assets['floor']), (x, y))
                if tile not in dynamic_objects: continue
                ObjectClass = dynamic_objects[tile]
                spawn_pos = (x + (cfg.TILE_SIZE // 2), y + (cfg.TILE_SIZE // 2))
                new_object = ObjectClass(
                    self.sprite_groups, self.assets, spawn_pos
                    )
                if ObjectClass is Player: player = new_object
        self._init_player(player)

    def resize(self):
        self.layout.update(self.screen.size)

    def _init_display(self):
        display_flags = pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE
        self.screen = pg.display.set_mode(
            cfg.START_SCREEN_SIZE, flags=display_flags, vsync=1
            )
        self.game_surf = pg.Surface((cfg.GAME_WIDTH, cfg.GAME_HEIGHT))
        self.layout = Layout(self.screen.size)
    
    def _init_assets(self):
        wall_face = pg.image.load('assets\\wall_face.png')
        shading = pg.Surface(wall_face.size)
        shading.fill((0, 0, 0))
        shading.set_alpha(100)
        wall_face.blit(shading)
        self.assets: Assets = {
            'floor': tuple(
                pg.image.load(f'assets\\grass\\{sprite}').convert()
                for sprite in listdir('assets\\grass')
                ),
            'wall_top': pg.image.load('assets\\wall_top.png').convert(),
            'wall_face': wall_face.convert(),
            'player': pg.transform.scale(
                pg.image.load('assets\\player.jpg'), (14, 14)
                ).convert(),
            'enemy': pg.transform.scale(
                pg.image.load('assets\\enemy.png'), (14, 14)
                ).convert_alpha(),
            'shotgun': pg.image.load('assets\\shotgun.png').convert_alpha(),
            'projectile': pg.image.load(
                'assets\\projectile.png'
                ).convert_alpha()
        }

    def _init_clock(self):
        self.clock = pg.time.Clock()
    
    def _init_sprite_groups(self):
        self.sprite_groups: SpriteGroups = {
            'rendering': pg.sprite.LayeredUpdates(),
            'obstacles': pg.sprite.Group(),
            'player': pg.sprite.GroupSingle(),
            'enemies': pg.sprite.Group(),
            'player_projectiles': pg.sprite.Group(),
            'enemy_projectiles': pg.sprite.Group()
        }

    def _init_camera(self):
        self.camera = Camera()

    def _init_player(self, player: Player):
        self.player = player
        for enemy in self.sprite_groups['enemies']:
            enemy.target = player


class Layout:
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