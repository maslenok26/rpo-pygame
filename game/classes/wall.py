from . import BaseSprite, HitboxSprite
from .. import config as cfg


class Wall(HitboxSprite):
    def __init__(self, sprite_groups, assets, pos):
        super().__init__(sprite_groups, assets, pos)

        self._layer = cfg.LAYERS['WALL_TOP']
        self.add_to_groups('rendering', 'obstacles')

        self.set_image(self.assets['wall_top'])

        Y_OFFSET = self.assets['wall_face'].height // 2

        self.hitbox = self.rect.move(0, Y_OFFSET)

        self.face = WallFace(
            sprite_groups, assets, (pos[0], self.rect.bottom+Y_OFFSET)
            )


class WallFace(BaseSprite):
    def __init__(self, sprite_groups, assets, pos):
        super().__init__(sprite_groups, assets, pos)

        self._layer = cfg.LAYERS['WALL_FACE']
        self.add_to_groups('rendering')

        self.set_image(self.assets['wall_face'])