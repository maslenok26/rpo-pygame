import pygame as pg
from ..settings import GAME_WIDTH, GAME_HEIGHT
from .player import Player

class Camera:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.pos = pg.Vector2(0, 0)
        self.rect = pg.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT)
        self.target_dist = pg.Vector2(0, 0)
        self.lerp_speed = 12.25
        self.mouse_lerp_strength = 0.25

    def get_offset(self):
        return (-self.rect.x, -self.rect.y)

    def adjust(self, sprite_rect: pg.Rect):
        return sprite_rect.move(self.get_offset())
    
    def _follow_mouse(self, mouse_pos: pg.Vector2, target_pos: pg.Vector2):
        return target_pos + round(mouse_pos * self.mouse_lerp_strength)
    
    def update(self, dt, target: Player, mouse_pos):
        lerp_value = min(self.lerp_speed * dt, 1)
        self.pos = (self.pos.lerp(
            self._follow_mouse(mouse_pos, target.pos), lerp_value
            ))
        self.target_dist = target.pos - self.pos
        self.rect.center = pg.Vector2(target.rect.center) - round(self.target_dist)