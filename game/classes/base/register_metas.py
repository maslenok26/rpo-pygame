from abc import ABCMeta

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .base_sprite import BaseSprite


class RegisterBaseMeta(type):
    def __call__(cls, *args, **kwargs):
        sprite: BaseSprite = super().__call__(*args, **kwargs)
        sprite.register()
        return sprite
    

class RegisterABCMeta(ABCMeta, RegisterBaseMeta):
    pass