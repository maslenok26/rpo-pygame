from pathlib import Path

import pygame as pg

from .. import config as cfg

ASSET_PATTERN = f'*{cfg.ASSET_SUFFIX}'

def load_assets(path, assets_dict=None, prefix=None):
    path = Path(path)
    if not path.is_dir():
        raise ValueError('Дерево ассетов должно быть директорией')
    if assets_dict is None: assets_dict = {}
    for subpath in path.iterdir():
        stem = subpath.stem
        key = (
            stem if prefix is None
            else prefix + cfg.ASSET_PATH_SEP + stem
        )
        if subpath.is_file() and subpath.suffix == cfg.ASSET_SUFFIX:
            assets_dict[key] = _load_image(subpath)
        elif subpath.is_dir():
            if subpath.suffix == cfg.SEQUENCE_SUFFIX:
                assets_dict[key] = _load_tuple(subpath)
            else:
                load_assets(subpath, assets_dict, prefix=key)
        else:
            raise ValueError('Неизвестный тип файла среди ассетов')
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