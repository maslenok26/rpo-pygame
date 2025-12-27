import pygame as pg
from ..settings import GAME_WIDTH, GAME_HEIGHT
from .player import Player

class Camera:
    def __init__(self):
        self.pos = pg.Vector2(0, 0)
        self.rect = pg.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT)
        self.lerp_speed = 12

    def adjust(self, sprite_rect: pg.Rect):
        return sprite_rect.move(-self.rect.x, -self.rect.y)
    
    def update(self, target: Player, dt):
        lerp_value = min(self.lerp_speed * dt, 1)
        self.pos = self.pos.lerp(target.pos, lerp_value)
        dist = target.pos - self.pos
        self.rect.centerx = target.rect.centerx - round(dist.x)
        self.rect.centery = target.rect.centery - round(dist.y)