from . import BaseSprite, HitboxSprite
from .. import config as cfg


class Wall(HitboxSprite):
    def __init__(self, sprite_groups, assets, pos, image_idx, needs_face):
        super().__init__(sprite_groups, assets, pos)

        Y_OFFSET = self._assets['walls']['face'].height // 2

        self._layer = cfg.LAYERS['WALL_TOP']
        self.add_to_groups('rendering', 'obstacles')

        self.set_image(self._assets['walls']['tops'][image_idx])
        self.rect.centery -= Y_OFFSET

        self._init_hitbox((cfg.TILE_SIZE, cfg.TILE_SIZE), pos)

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
        super().__init__(sprite_groups, assets, pos)

        self._layer = cfg.LAYERS['WALL_FACE']
        self.add_to_groups('rendering')

        self.set_image(self._assets['walls']['face'])