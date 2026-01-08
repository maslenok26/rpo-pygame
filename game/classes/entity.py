from abc import ABC

from .body import Body


class Entity(Body, ABC):
    def __init__(self, sprite_groups):
        super().__init__(sprite_groups)
        self.hp = 0
        self.damage = 0
        self.is_dead = False

        self.image_flipped = False

    def take_damage(self, amount):
        if self.is_dead: return
        self.hp -= amount
        if self.hp <= 0:
            self.die()
    
    def die(self):
        self.kill()
        self.is_dead = True

    def _handle_collision(self, _):
        return 'STOP'