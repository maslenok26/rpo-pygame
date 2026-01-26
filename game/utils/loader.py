from pathlib import Path

import pygame as pg


def load_folder(path):
    folder = tuple(
        _load_image(file)
        for file in sorted(Path(path).glob('*.png'))
    )
    return folder

def load_asset(file):
    return (_load_image(file),)

def _load_image(file):
    image = pg.image.load(file)
    if image.get_alpha() is not None:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image