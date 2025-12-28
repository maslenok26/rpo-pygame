import pygame as pg
from .settings import *
from .classes import *
from .utils import scale_surface

class GameManager:
    def __init__(self):
        self._init_display()
        self._init_clock()
        self._init_sprites()
        self._init_camera()
        self._init_level()

    def _init_display(self):
        display_flags = pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE
        self.screen = pg.display.set_mode(
            (START_SCREEN_WIDTH, START_SCREEN_HEIGHT), flags=display_flags, vsync=1
            )
        self.game_surf = pg.Surface((GAME_WIDTH, GAME_HEIGHT))

    def _init_clock(self):
        self.clock = pg.time.Clock()
    
    def _init_sprites(self):
        self.all_sprites: pg.sprite.Group[pg.sprite.Sprite] = pg.sprite.Group()
        self.collidables: pg.sprite.Group[pg.sprite.Sprite] = pg.sprite.Group()
        self.groups = (self.all_sprites, self.collidables)

    def _init_camera(self):
        self.camera = Camera(self.screen)

    def _init_level(self, level_map: list[str]=TEST_MAP):
        for group in self.groups:
            group.empty()
        tiles = {
            'W': (Wall, (self.all_sprites, self.collidables)),
            'P': (Player, self.all_sprites)
            # ...
        }
        for y, row in enumerate(level_map):
            for x, tile in enumerate(row.split()):
                if tile not in tiles: continue
                ObjectClass, groups = tiles[tile]
                new_object = ObjectClass(x, y, groups)
                if ObjectClass is Player:
                    self.player: Player = new_object

    def get_fps(self):
        return FPS if FPS_LOCK else 0
    
    def _draw(self):
        self.game_surf.fill((0, 0, 0))
        for sprite in self.all_sprites:
            self.game_surf.blit(sprite.image, self.camera.adjust(sprite.rect))
        scaled_surf, offset = scale_surface(self.screen, self.game_surf)
        self.screen.fill((0, 0, 0))
        self.screen.blit(scaled_surf, offset)
    
    def update(self, dt):
        self.player.update(self.collidables, dt)
        self.camera.update(self.player, dt)
        self._draw()