import pygame as pg
from .settings import *
from .utils import transform_image

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, groups):
        super().__init__(groups)
        self.image = transform_image('vanya.jpg', (TILE_SIZE*1.5, TILE_SIZE*1.5))
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))
        self.pos = pg.Vector2(self.rect.center)
        self.x_rem = 0
        self.y_rem = 0
        self.vector = pg.Vector2(0, 0)
        self.base_speed = TILE_SIZE * 9
        self.speed = self.base_speed
        self.is_dashing = False
        self.dash_speed = self.base_speed * 2.5
        self.dash_duration = 75
        self.dash_cooldown = 1000
        self.last_dash_time = -self.dash_cooldown

    def get_input(self):
        if self.is_dashing:
            return
        self.vector.x, self.vector.y = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_w]: self.vector.y -= 1
        if keys[pg.K_a]: self.vector.x -= 1
        if keys[pg.K_s]: self.vector.y += 1
        if keys[pg.K_d]: self.vector.x += 1
        if self.vector.length():
            self.vector = self.vector.normalize()
            if keys[pg.K_SPACE]: self.dash()

    def _make_a_step(self, axis, step, move, moved, collidables):
        if axis == 'x': self.rect.x += step
        elif axis == 'y': self.rect.y += step
        if not pg.sprite.spritecollide(self, collidables, False):
            moved += step
            move -= step
        else:
            if axis == 'x':
                self.rect.x -= step
                self.x_rem = 0
            elif axis == 'y':
                self.rect.y -= step
                self.y_rem = 0
            move = 0
        return move, moved

    def move(self, dt, collidables):
        delta_x = self.vector.x * self.speed * dt
        delta_y = self.vector.y * self.speed * dt
        self.x_rem += delta_x
        self.y_rem += delta_y
        moved_x = 0
        moved_y = 0
        move_x = int(self.x_rem)
        move_y = int(self.y_rem)
        step_x = SUB_STEP if move_x > 0 else -SUB_STEP
        step_y = SUB_STEP if move_y > 0 else -SUB_STEP
        while move_x or move_y:
            if move_x: move_x, moved_x = self._make_a_step('x', step_x, move_x, moved_x, collidables)
            if move_y: move_y, moved_y = self._make_a_step('y', step_y, move_y, moved_y, collidables)
        self.x_rem -= moved_x
        self.y_rem -= moved_y
        self.pos.x = self.rect.centerx + self.x_rem
        self.pos.y = self.rect.centery + self.y_rem

    def dash(self):
        cur_time = pg.time.get_ticks()
        if cur_time - self.last_dash_time <= self.dash_cooldown:
            return
        self.speed = self.dash_speed
        self.is_dashing = True
        self.last_dash_time = cur_time

    def check_dash(self):
        if not self.is_dashing:
            return
        cur_time = pg.time.get_ticks()
        if cur_time - self.last_dash_time < self.dash_duration:
            return
        self.speed = self.base_speed
        self.is_dashing = False

    def update(self, dt, collidables):
        self.get_input()
        self.move(dt, collidables)


class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, groups):
        super().__init__(groups)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))
        self.pos = pg.Vector2(self.rect.center)


class Camera:
    def __init__(self):
        self.pos = pg.math.Vector2(0, 0)
        self.rect = pg.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT)
        self.lerp_speed = 12

    def adjust(self, sprite):
        return sprite.rect.move(-self.rect.x, -self.rect.y)

    def update(self, target, dt):
        lerp_value = self.lerp_speed * dt
        if lerp_value > 1: lerp_value = 0
        self.pos = self.pos.lerp(target.rect.center, lerp_value) * (1 + pow(10, -14))
        self.rect.center = (int(self.pos.x), int(self.pos.y))