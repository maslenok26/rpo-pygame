import pygame as pg
from .settings import TILE_SIZE

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((50, 50))
        self.image.fill((150, 255, 150))
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))
        self.pos = pg.math.Vector2(self.rect.center)
        self.vector = pg.math.Vector2(0, 0)
        self.speed = 350

    def get_input(self):
        self.vector.x, self.vector.y = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vector.y -= 1
        if keys[pg.K_a]:
            self.vector.x -= 1
        if keys[pg.K_s]:
            self.vector.y += 1
        if keys[pg.K_d]:
            self.vector.x += 1
        if self.vector.length() != 0:
            self.vector = self.vector.normalize()

    def check_collisions(self, direction, collided_sprites):
        if not collided_sprites:
            return
        for sprite in collided_sprites:
            if direction == 'h':
                if self.vector.x > 0:
                    self.rect.right = sprite.rect.left
                else:
                    self.rect.left = sprite.rect.right
                self.pos.x = self.rect.centerx
            elif direction == 'v':
                if self.vector.y > 0:
                    self.rect.bottom = sprite.rect.top
                else:
                    self.rect.top = sprite.rect.bottom
                self.pos.y = self.rect.centery

    def move(self, dt, collidables):
        self.pos.x  += self.vector.x * self.speed * dt
        self.rect.centerx = round(self.pos.x)
        collided_sprites = pg.sprite.spritecollide(self, collidables, False)
        self.check_collisions('h', collided_sprites)
        self.pos.y += self.vector.y * self.speed * dt
        self.rect.centery = round(self.pos.y)
        collided_sprites = pg.sprite.spritecollide(self, collidables, False)
        self.check_collisions('v', collided_sprites)

    def update(self, dt, collidables):
        self.get_input()
        self.move(dt, collidables)


class Wall(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))