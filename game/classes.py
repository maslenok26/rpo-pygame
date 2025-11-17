import pygame as pg
from .settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((TILE_SIZE//1.5, TILE_SIZE//1.5))
        self.image.fill((150, 255, 150))
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))
        self.pos = pg.math.Vector2(self.rect.center)
        self.vector = pg.math.Vector2(0, 0)
        self.base_speed = TILE_SIZE * 9
        self.speed = self.base_speed
        self.is_dashing = False
        self.dash_speed = self.base_speed * 2.5
        self.dash_duration = 75
        self.dash_cooldown = 1000
        self.last_dash_time = -self.dash_cooldown

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
            if keys[pg.K_SPACE]:
                self.dash()
        
    def check_collisions(self, axis, collided_sprites):
        if not collided_sprites:
            return
        for sprite in collided_sprites:
            if axis == 'x':
                if self.vector.x > 0:
                    self.rect.right = sprite.rect.left
                else:
                    self.rect.left = sprite.rect.right
                self.pos.x = self.rect.centerx
            elif axis == 'y':
                if self.vector.y > 0:
                    self.rect.bottom = sprite.rect.top
                else:
                    self.rect.top = sprite.rect.bottom
                self.pos.y = self.rect.centery

    def move(self, dt, collidables):
        self.pos.x  += self.vector.x * self.speed * dt
        self.rect.centerx = round(self.pos.x)
        collided_sprites = pg.sprite.spritecollide(self, collidables, False)
        self.check_collisions('x', collided_sprites)
        self.pos.y += self.vector.y * self.speed * dt
        self.rect.centery = round(self.pos.y)
        collided_sprites = pg.sprite.spritecollide(self, collidables, False)
        self.check_collisions('y', collided_sprites)
    
    def dash(self):
        cur_time = pg.time.get_ticks()
        if cur_time - self.last_dash_time <= self.dash_cooldown:
            return
        self.speed = self.dash_speed
        self.is_dashing = True
        self.last_dash_time = cur_time
    
    def check_dash(self):
        cur_time = pg.time.get_ticks()
        if cur_time - self.last_dash_time <= self.dash_duration:
            return
        self.speed = self.base_speed
        self.is_dashing = False
        
    def update(self, dt, collidables):
        self.get_input()
        self.move(dt, collidables)


class Wall(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))


class Camera:
    def __init__(self):
        self.rect = pg.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT)
    
    def adjust(self, sprite):
        return sprite.rect.move(-self.rect.x, -self.rect.y)
    
    def update(self, player):
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery