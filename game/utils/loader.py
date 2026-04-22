from pathlib import Path

import pygame as pg

from .. import config as cfg

ASSET_PATTERN = f'*{cfg.ASSET_SUFFIX}'

def load_tree(path):
    path = Path(path)
    assets_dict = {}
    if not path.is_dir():
        raise ValueError('Дерево ассетов должно быть директорией')
    for subpath in path.iterdir():
        key = subpath.stem
        if subpath.is_file() and subpath.suffix == cfg.ASSET_SUFFIX:
            assets_dict[key] = _load_image(subpath)
        elif subpath.is_dir():
            if subpath.suffix == cfg.SEQUENCE_SUFFIX:
                assets_dict[key] = _load_tuple(subpath)
            else:
                assets_dict[key] = load_tree(subpath)
    return assets_dict

def _load_tuple(path):
    assets = tuple(
        _load_image(asset)
        for asset in _get_assets(path)
    )
    return assets

def _load_image(path):
    image = pg.image.load(path)
    if image.get_alpha() is None:
        return image.convert()
    return image.convert_alpha()

def _get_assets(path: Path):
    return sorted(path.glob(ASSET_PATTERN))