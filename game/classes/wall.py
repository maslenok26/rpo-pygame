from . import BaseSprite, HitboxSprite
from ..dynamic_assets import generate_obstacle_shadow
from .. import config as cfg


class Wall(HitboxSprite):
    def __init__(self, sprite_groups, assets, pos, depth, needs_face):
        stats = cfg.WALL
        self.image_idx = depth

        super().__init__(sprite_groups, assets, pos, stats)

        self._add_to_groups('obstacles')

        if needs_face:
            self.face = BaseSprite(
                sprite_groups, assets, self.rect.midbottom, cfg.WALL_FACE
            )
            shadow_stats = (
                self._get_shadow_stats(generate_obstacle_shadow)
            )
            self.shadow = BaseSprite(
                sprite_groups, assets, self.face.rect.midbottom, shadow_stats
            )
            self.kill = self._kill_with_components
        # стена сдвигается на оффсет. благодаря тому что сдвиг происходит в
        # конце, лицо и тень стены остаются на нужных местах.
        self.rect.centery -= stats['render']['y_offset']

    def _kill_with_components(self):
        self.face.kill()
        self.shadow.kill()
        super().kill()