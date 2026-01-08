import pygame as pg

from .base_sprite import BaseSprite
from .hitbox_sprite import HitboxSprite
from ..settings import LAYERS, TILE_SIZE


class Wall:
    def __init__(self, sprite_groups, x, y):
        WallTop(sprite_groups, x, y)
        WallFace(sprite_groups, x, y+1)


class WallTop(HitboxSprite):
    def __init__(self, sprite_groups, x, y):
        super().__init__(sprite_groups)

        self._layer = LAYERS['WALL_TOP']
        self.add_to_groups('rendering', 'collidables')

        self.image = pg.image.load('assets\\wall.png')
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))

        self.hitbox = self.rect.move(0, 5)


class WallFace(BaseSprite):
    def __init__(self, sprite_groups, x, y):
        super().__init__(sprite_groups)

        self._layer = LAYERS['WALL_FACE']
        self.add_to_groups('rendering')

        self.image = pg.image.load('assets\\wall_face.png')
        shading = pg.Surface(self.image.get_size())
        shading.fill((0, 0, 0))
        shading.set_alpha(100)
        self.image.blit(shading)
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))