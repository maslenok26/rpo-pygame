import pygame as pg


def scale_image(path, size):
    image = pg.image.load(f'assets\\{path}').convert_alpha()
    size = (int(size[0]), int(size[1]))
    return pg.transform.scale(image, size)