from . import BaseSprite
from .. import config as cfg


class Shadow(BaseSprite):
    _layer = cfg.LAYERS['shadow']

    def __init__(self, sprite_groups, assets, pos, stats):
        super().__init__(sprite_groups, assets, pos, stats)

        self._add_to_groups('rendering')