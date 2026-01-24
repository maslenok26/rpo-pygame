from . import BaseSprite, HitboxSprite
from .. import config as cfg


class Wall(HitboxSprite):
    def __init__(self, sprite_groups, assets, pos, depth, needs_face):
        stats = cfg.WALL
        self.image_idx = depth

        super().__init__(sprite_groups, assets, pos, stats)

        Y_OFFSET = self._assets['walls']['face'][0].height // 2

        self._layer = cfg.LAYERS['wall_top']
        self._add_to_groups('rendering', 'obstacles')

        self.rect.centery -= Y_OFFSET

        if needs_face:
            self.face = WallFace(
                sprite_groups, assets, (pos[0], self.rect.bottom+Y_OFFSET)
            )
            self.kill = self._kill_with_face

    def _kill_with_face(self):
        self.face.kill()
        super().kill()


class WallFace(BaseSprite):
    def __init__(self, sprite_groups, assets, pos):
        stats = cfg.WALL_FACE

        super().__init__(sprite_groups, assets, pos, stats)

        self._layer = cfg.LAYERS['wall_face']
        self._add_to_groups('rendering')