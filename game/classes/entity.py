from abc import ABC

from .body import Body


class Entity(Body, ABC):
    def _handle_collision(self):
        return 'STOP'