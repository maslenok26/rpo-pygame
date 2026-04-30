import pygame as pg

from .. import config as cfg

def generate_obstacle_shadow(image: pg.Surface):
    shadow_surf = pg.transform.flip(image, flip_x=False, flip_y=True)
    shadow_surf.fill(cfg.SHADOW_COLOR_RGBA)
    return shadow_surf

def generate_entity_shadow(image: pg.Surface):
    bounding_rect = image.get_bounding_rect()
    width = bounding_rect.width
    height = int(width * 0.3)
    shadow_surf = pg.Surface((width, height), pg.SRCALPHA)
    pg.draw.ellipse(shadow_surf, cfg.SHADOW_COLOR_RGBA, (0, 0, width, height))
    return shadow_surf