import pygame as pg

from ..settings import TILE_SIZE


class Wall(pg.sprite.Sprite):
    def __init__(self, sprite_groups, x, y):
        super().__init__((sprite_groups['all'], sprite_groups['collidables']))
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((75, 75, 75))
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))