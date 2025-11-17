import pygame as pg
from .settings import GAME_WIDTH, GAME_HEIGHT

def transform_image(path, size):
    return pg.transform.scale(pg.image.load(f'assets\\{path}').convert_alpha(), (size[0], size[1]))

def transform_surface(root, surface):
    cur_size_x, cur_size_y = root.get_size()
    scale_x, scale_y = cur_size_x / GAME_WIDTH, cur_size_y / GAME_HEIGHT
    scale = max(scale_x, scale_y)
    scaled_width = GAME_WIDTH * scale
    scaled_height = GAME_HEIGHT * scale
    scaled_surface = pg.transform.scale(surface, (scaled_width, scaled_height))
    offset_x, offset_y = (cur_size_x - scaled_width) // 2, (cur_size_y - scaled_height) // 2
    return scaled_surface, (offset_x, offset_y)