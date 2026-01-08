import pygame as pg

from .body import Body
from .timer import Timer
from ..settings import LAYERS


class Projectile(Body):
    def __init__(self, sprite_groups, x, y, vector: pg.Vector2):
        super().__init__(sprite_groups)

        self._layer = LAYERS['PROJECTILE']
        self.add_to_groups('rendering', 'projectiles')

        self.speed = 150

        self.orig_image = pg.image.load('assets\\projectile.png').convert_alpha()
        self.image = pg.transform.rotate(self.orig_image, -vector.angle)
        self.rect = self.image.get_rect(center=(x, y))

        self._create_hitbox(8, 6, self.rect.center)
        is_colliding = pg.sprite.spritecollideany(
            self,
            sprite_groups['collidables'], 
            collided=self._check_hitbox_collision
            )
        if is_colliding: self.kill()

        self.pos = pg.math.Vector2(self.rect.center)
        self.vector = vector

        self.timers = {
            'lifetime': Timer(
                duration=3000, end_func=self.kill, cooldown=0
            )
        }

        self.timers['lifetime'].start()
    
    def update(self, dt, collidables):
        self._move(dt, collidables)
        self.timers['lifetime'].update()
    
    def _handle_collision(self):
        self.image = pg.transform.rotate(self.orig_image, self.vector.angle)
        return 'BOUNCE'