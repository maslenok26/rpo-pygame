import pygame as pg
from math import copysign
from ..settings import TILE_SIZE, SUB_STEP
from ..utils import scale_image

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, groups):
        super().__init__(groups)
        self.image = scale_image('vanya.jpg', (TILE_SIZE*1.3, TILE_SIZE*1.3))
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))
        self.pos = pg.Vector2(self.rect.center)
        self.rem_x = 0
        self.rem_y = 0
        self.vector = pg.Vector2(0, 0)
        self.base_speed = TILE_SIZE * 10
        self.speed = self.base_speed
        self.is_dashing = False
        self.dash_speed = self.base_speed * 2.5
        self.dash_duration = 75
        self.dash_cooldown = 1000
        self.last_dash_time = -self.dash_cooldown

    def get_input(self):
        if self.is_dashing: return
        self.vector *= 0
        keys = pg.key.get_pressed()
        if keys[pg.K_w]: self.vector.y -= 1
        if keys[pg.K_a]: self.vector.x -= 1
        if keys[pg.K_s]: self.vector.y += 1
        if keys[pg.K_d]: self.vector.x += 1
        if self.vector.length():
            self.vector = self.vector.normalize()
            if keys[pg.K_SPACE]: self.dash()

    def _make_a_step(self, axis, step, steps_to_do, steps_done, collidables):
        if axis == 'x': self.rect.x += step
        elif axis == 'y': self.rect.y += step
        if not pg.sprite.spritecollide(self, collidables, False):
            steps_done += step
            steps_to_do -= step
        else:
            if axis == 'x':
                self.rect.x -= step
                self.rem_x = 0
            elif axis == 'y':
                self.rect.y -= step
                self.rem_y = 0
            steps_to_do = 0
        return steps_to_do, steps_done

    def move(self, dt, collidables):
        self.rem_x += self.vector.x * self.speed * dt
        self.rem_y += self.vector.y * self.speed * dt
        steps_to_do_x = round(self.rem_x)
        steps_to_do_y = round(self.rem_y)
        steps_done_x = 0
        steps_done_y = 0
        step_x = copysign(SUB_STEP, steps_to_do_x)
        step_y = copysign(SUB_STEP, steps_to_do_y)
        while steps_to_do_x or steps_to_do_y:
            if steps_to_do_x: steps_to_do_x, steps_done_x = self._make_a_step(
                'x', step_x, steps_to_do_x, steps_done_x, collidables
                )
            if steps_to_do_y: steps_to_do_y, steps_done_y = self._make_a_step(
                'y', step_y, steps_to_do_y, steps_done_y, collidables
                )
        self.rem_x -= steps_done_x
        self.rem_y -= steps_done_y
        self.pos.x = self.rect.centerx + self.rem_x
        self.pos.y = self.rect.centery + self.rem_y
        
    def dash(self):
        cur_time = pg.time.get_ticks()
        if cur_time - self.last_dash_time <= self.dash_cooldown: return
        self.speed = self.dash_speed
        self.is_dashing = True
        self.last_dash_time = cur_time

    def check_dash(self):
        if not self.is_dashing: return
        cur_time = pg.time.get_ticks()
        if cur_time - self.last_dash_time < self.dash_duration: return
        self.speed = self.base_speed
        self.is_dashing = False

    def update(self, dt, collidables):
        self.get_input()
        self.move(dt, collidables)
        self.check_dash()