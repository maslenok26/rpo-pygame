from os import listdir
from random import choice

import pygame as pg

from .classes import *
from .settings import *
from .utils import get_scale, scale_surface


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
    
    def get_mouse_pos(self):
        scale = get_scale(self.screen.width, self.screen.height)
        offset = pg.Vector2(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        return (pg.Vector2(pg.mouse.get_pos()) / scale) - offset
    
    def update(self, dt):
        self.player.update(dt, self.collidable_sprites)
        mouse_pos = self.get_mouse_pos()
        self.camera.update(dt, self.player, mouse_pos)
        self.player.animate(mouse_pos, self.camera.target_dist.x)

    def draw(self):
        self.game_surf.fill((0, 0, 0))
        self.game_surf.blit(self.static_surf, self.camera.get_offset())
        for sprite in self.all_sprites:
            self.game_surf.blit(sprite.image, self.camera.adjust(sprite.rect))
        scaled_surf, scaling_offset = scale_surface(self.screen, self.game_surf)
        self.screen.fill((0, 0, 0))
        self.screen.blit(scaled_surf, scaling_offset)

    def _init_display(self):
        display_flags = pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE
        self.screen = pg.display.set_mode(
            (START_SCREEN_WIDTH, START_SCREEN_HEIGHT), flags=display_flags, vsync=1
            )
        self.game_surf = pg.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.static_surf = pg.Surface((GAME_WIDTH, GAME_HEIGHT))

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
        self.all_sprites: pg.sprite.Group[pg.sprite.Sprite] = pg.sprite.Group()
        self.collidable_sprites = pg.sprite.Group()
        self.groups = (self.all_sprites, self.collidable_sprites)

    def _init_camera(self):
        self.camera = Camera()

    def _init_level(self, level_map: list[str]=TEST_MAP):
        for group in self.groups:
            group.empty()
        dynamic_tiles = {
            'W': (Wall, (self.all_sprites, self.collidable_sprites)),
            'P': (Player, self.all_sprites)
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