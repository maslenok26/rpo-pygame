from __future__ import annotations

import pygame as pg

from .. import config as cfg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player


class Camera:
    def __init__(self):
        self.lerp_speed = 12.25
        self.mouse_sensitivity = 0.35

        self.rect = pg.Rect(0, 0, cfg.GAME_WIDTH, cfg.GAME_HEIGHT)
        
        self.pos = pg.Vector2()

        self.target_dist = pg.Vector2()

    def get_offset(self):
        return -self.rect.x, -self.rect.y
    
    def update(self, dt, target: Player, mouse_pos: pg.Vector2):
        lerp_value = min(self.lerp_speed*dt, 1)
        self.pos = self.pos.lerp(
            target.pos + round(mouse_pos * self.mouse_sensitivity),
            lerp_value
            )
        self.target_dist = round(target.pos - self.pos)
        self.rect.center = target.rect.center - self.target_dist