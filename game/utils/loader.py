from pathlib import Path

import pygame as pg


def load_folder(path):
    folder = tuple(
        _load_surface(file)
        for file in sorted(Path(path).glob('*.png'))
    )
    return folder

def load_image(file):
    return (_load_surface(file),)

def _load_surface(file):
    surf = pg.image.load(file)
    if surf.get_alpha() is not None:
        surf = surf.convert_alpha()
    else:
        surf = surf.convert()
    return surf