import pygame as pg


class Timer:
    def __init__(
            self, duration, end_func, cooldown, can_overlap=False
            ):
        self.duration = duration
        self.end_func = end_func
        self.cooldown = cooldown
        self.can_overlap = can_overlap

        self.active = False
        self._start_time = 0
        self._end_time = -cooldown

    def start(self):
        if self.active and not self.can_overlap:
            return False
        cur_time = pg.time.get_ticks()
        if cur_time - self._end_time < self.cooldown:
            return False
        self.active = True
        self._start_time = cur_time
        return True

    def update(self):
        if not self.active: return
        cur_time = pg.time.get_ticks()
        if cur_time - self._start_time >= self.duration:
            self._stop(cur_time)

    def _stop(self, cur_time):
        self.active = False
        self._end_time = cur_time
        if self.end_func:
            self.end_func()