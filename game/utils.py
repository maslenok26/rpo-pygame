import pygame as pg

from .settings import GAME_WIDTH, GAME_HEIGHT


def scale_image(path, size):
    image = pg.image.load(f'assets\\{path}').convert_alpha()
    size = (int(size[0]), int(size[1]))
    return pg.transform.scale(image, size)

def get_scale(width, height):
    scale_x, scale_y = width / GAME_WIDTH, height / GAME_HEIGHT
    return max(scale_x, scale_y)

def scale_surface(root: pg.Surface, surface):
    cur_width, cur_height = root.get_size()
    scale = get_scale(cur_width, cur_height)
    scaled_width = GAME_WIDTH * scale
    scaled_height = GAME_HEIGHT * scale
    scaled_surface = pg.transform.scale(surface, (scaled_width, scaled_height))
    offset_x = (cur_width - scaled_width) // 2
    offset_y = (cur_height - scaled_height) // 2
    return scaled_surface, (offset_x, offset_y)