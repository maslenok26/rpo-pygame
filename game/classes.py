import pygame as pg
from .settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.orig_image = pg.Surface((TILE_SIZE//1.5, TILE_SIZE//1.5))
        self.orig_image.fill((150, 255, 150))
        self.image = self.orig_image.copy()
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))
        self.pos = pg.math.Vector2(self.rect.center)
        self.vector = pg.math.Vector2(0, 0)
        self.base_speed = TILE_SIZE * 9
        self.speed = self.base_speed
        self.is_dashing = False
        self.dash_speed = self.base_speed * 3
        self.dash_duration = 70
        self.dash_cooldown = 800
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
        self.orig_image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.orig_image.fill((100, 100, 100))
        self.image = self.orig_image.copy()
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))
        self.pos = pg.math.Vector2(self.rect.center)


# class Camera:
#     def __init__(self):
#         self.rect = pg.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT)
    
#     def adjust(self, sprite):
#         return sprite.rect.move(-self.rect.x, -self.rect.y)
    
#     def update(self, player):
#         self.pos = player.pos


class Camera:
    def __init__(self):
        self.offset = pg.math.Vector2(0, 0) # Позиция камеры в мире логики (float)

    def update(self, player):
        # Камера пытается удержать игрока в центре своего вида
        self.offset.x = player.pos.x - (GAME_WIDTH / 2)
        self.offset.y = player.pos.y - (GAME_HEIGHT / 2)

    def get_render_pos(self, sprite, scale):
        # --- Шаг 1: Найти левый верхний угол спрайта в мире логики ---
        
        # Размер спрайта в мире логики (например, 16x16)
        sprite_width_low = sprite.orig_image.get_width()
        sprite_height_low = sprite.orig_image.get_height()
        
        # Позиция левого верхнего угла в мире логики (float)
        sprite_topleft_low_x = sprite.pos.x - (sprite_width_low / 2)
        sprite_topleft_low_y = sprite.pos.y - (sprite_height_low / 2)

        # --- Шаг 2: Найти позицию относительно камеры ---
        
        # Вычитаем смещение камеры, чтобы получить позицию "на экране"
        # но все еще в координатах мира логики (float)
        render_pos_low_x = sprite_topleft_low_x - self.offset.x
        render_pos_low_y = sprite_topleft_low_y - self.offset.y

        # --- Шаг 3: Перевести позицию в координаты экрана (High-Res) ---
        
        # Умножаем "экранную" позицию из мира логики на масштаб
        # и превращаем в целое число для blit.
        screen_x = render_pos_low_x * scale
        screen_y = render_pos_low_y * scale

        return (screen_x, screen_y)