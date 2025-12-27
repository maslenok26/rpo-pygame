import pygame as pg
from .settings import *
from .classes import *

pg.display.init()

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

    def _init_camera(self):
        self.camera = Camera()

    def _init_level(self, map: str=TEST_MAP):
        self.all_sprites.empty()
        self.collidables.empty()
        for y, row in enumerate(map):
            for x, tile in enumerate(row.split()):
                if tile == 'W':
                    Wall(x, y, (self.all_sprites, self.collidables))
                elif tile == 'P':
                    self.player = Player(x, y, (self.all_sprites))

    def get_fps(self):
        return FPS if FPS_LOCK else 0
    
game_manager = GameManager()