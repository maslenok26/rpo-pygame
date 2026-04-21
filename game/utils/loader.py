from pathlib import Path

import pygame as pg


def load_dict(path):
    assets = {
        file.stem: load_asset(file)
        for file in _get_files(path)
    }
    return assets

def load_arr(path):
    assets = tuple(
        _load_image(file)
        for file in sorted(_get_files(path))
    )
    return assets

def load_asset(file):
    return (_load_image(file),)

def _get_files(path):
    return Path(path).glob('*.png')

def _load_image(file):
    image = pg.image.load(file)
    if image.get_alpha() is not None:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image