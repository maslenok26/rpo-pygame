from __future__ import annotations

from . import UISprite
from .. import config as cfg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Player


class HPBar:
    def __init__(self, sprite_groups, assets, owner):
        stats = cfg.HUD['hp_bar']

        UISprite(sprite_groups, assets, stats['outer'])
        self._HPBarInner(sprite_groups, assets, stats['inner'], owner)


    class _HPBarInner(UISprite):
        def __init__(self, sprite_groups, assets, stats, owner: Player):
            super().__init__(sprite_groups, assets, stats)

            self.owner = owner
            self.max_owner_hp = self.owner.hp
            self._update_prev_owner_hp()

        def update(self):
            cur_owner_hp = self.owner.hp
            if self.prev_owner_hp == cur_owner_hp: return
            ratio = cur_owner_hp / self.max_owner_hp
            self._update_prev_owner_hp()
            self._set_image(
                self._orig_image.subsurface(
                    0, 0, self._orig_image.width*ratio, self.image.height
                )
            )
        
        def _update_prev_owner_hp(self):
            self.prev_owner_hp = self.owner.hp