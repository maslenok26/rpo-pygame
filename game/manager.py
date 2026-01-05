from os import listdir
from random import choice

import pygame as pg

from .classes import *
from .settings import *


class GameManager:
    def __init__(self):
        self._init_display()
        self._init_assets()
        self._init_clock()
        self._init_sprites()
        self._init_camera()
        self._init_level()

    def get_fps(self):
        return FPS if FPS_LOCK else 0
    
    def get_mouse_screen_pos(self):
        mouse_pos: pg.Vector2 = (
            (pg.Vector2(pg.mouse.get_pos()) - self.layout['offset']) 
            / self.layout['scale']
        )
        mouse_pos.x = pg.math.clamp(mouse_pos.x, 0, GAME_WIDTH)
        mouse_pos.y = pg.math.clamp(mouse_pos.y, 0, GAME_HEIGHT)
        game_surf_center = pg.Vector2(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        screen_pos = mouse_pos - game_surf_center
        return screen_pos
    
    def update(self, dt):
        self.player.update(dt, self.sprites['collidables'])
        mouse_screen_pos = self.get_mouse_screen_pos()
        self.camera.update(dt, self.player, mouse_screen_pos)
        self.player.animate(mouse_screen_pos, self.camera.target_dist)

    def draw(self):
        self.game_surf.fill((0, 0, 0))
        self.screen.fill((0, 0, 0))
        camera_offset = self.camera.get_offset()
        self.game_surf.blit(self.static_surf, camera_offset)
        for sprite in self.sprites['all']:
            self.game_surf.blit(sprite.image, sprite.rect.move(camera_offset))
        scaled_game_surf = pg.transform.scale(
            self.game_surf, self.layout['size']
            )
        self.screen.blit(scaled_game_surf, self.layout['offset'])
    
    def update_layout(self):
        scales = (
            self.screen.width / GAME_WIDTH, self.screen.height / GAME_HEIGHT
            )
        scale = min(scales) if LETTERBOXING else max(scales)
        scaled_width = GAME_WIDTH * scale
        scaled_height = GAME_HEIGHT * scale
        offset_x = (self.screen.width - scaled_width) // 2
        offset_y = (self.screen.height - scaled_height) // 2
        self.layout['scale'] = scale
        self.layout['offset'] = pg.Vector2(offset_x, offset_y)
        self.layout['size'] = (int(scaled_width), int(scaled_height))

    def _init_display(self):
        display_flags = pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE
        self.screen = pg.display.set_mode(
            (START_SCREEN_WIDTH, START_SCREEN_HEIGHT),
            flags=display_flags,
            vsync=1
            )
        self.game_surf = pg.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.static_surf = pg.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.layout = {}
        self.update_layout()

    def _init_assets(self):
        self.assets = {
            'grass': tuple(
                pg.image.load(f'assets\\grass\\{sprite}').convert_alpha()
                for sprite in listdir('assets\\grass')
                )
        }

    def _init_clock(self):
        self.clock = pg.time.Clock()
    
    def _init_sprites(self):
        self.sprites: dict[str, pg.sprite.Group[pg.sprite.Sprite]] = {
            'all': pg.sprite.Group(),
            'collidables': pg.sprite.Group()
        }

    def _init_camera(self):
        self.camera = Camera()

    def _init_level(self, level_map: list[str]=TEST_MAP):
        for sprite_group in self.sprites.values():
            sprite_group.empty()
        dynamic_tiles = {
            'W': (Wall, (self.sprites['all'], self.sprites['collidables'])),
            'P': (Player, self.sprites['all'])
        }
        for y, row in enumerate(level_map):
            for x, tile in enumerate(row.split()):
                self.static_surf.blit(
                    choice(self.assets['grass']),
                    (x*TILE_SIZE, y*TILE_SIZE)
                    )
                if tile not in dynamic_tiles: continue
                ObjectClass, groups = dynamic_tiles[tile]
                new_object = ObjectClass(x, y, groups)
                if ObjectClass is Player:
                    self.player: Player = new_object