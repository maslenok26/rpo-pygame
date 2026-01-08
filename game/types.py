from typing import TypedDict

import pygame as pg


class SpriteGroups(TypedDict):
    rendering: pg.sprite.LayeredUpdates[pg.sprite.Sprite]
    collidables: pg.sprite.Group[pg.sprite.Sprite]
    projectiles: pg.sprite.Group[pg.sprite.Sprite]