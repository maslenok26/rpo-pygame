import pygame as pg
from ..settings import GAME_WIDTH, GAME_HEIGHT
from .player import Player
from ..utils import get_scale

class Camera:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.pos = pg.Vector2(0, 0)
        self.rect = pg.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT)
        self.lerp_speed = 12
        self.mouse_lerp_strength = 0.2

    def adjust(self, sprite_rect: pg.Rect):
        return sprite_rect.move(-self.rect.x, -self.rect.y)
    
    def _follow_mouse(self, pos):
        scale = get_scale(self.screen.width, self.screen.height)
        offset = pg.Vector2(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        mouse_pos = (pg.Vector2(pg.mouse.get_pos()) / scale) - offset
        return pos + (round(mouse_pos) * self.mouse_lerp_strength)
    
    def update(self, target: Player, dt):
        lerp_value = min(self.lerp_speed * dt, 1)
        self.pos = (self.pos.lerp(self._follow_mouse(target.pos), lerp_value))
        dist = target.pos - self.pos
        self.rect.centerx = target.rect.centerx - round(dist.x)
        self.rect.centery = target.rect.centery - round(dist.y)