from math import dist, copysign
from random import random, choice, sample

import pygame as pg

from .. import config as cfg


class LevelGenerator:
    SAFE_LAYER = 4

    def __init__(
            self,
            width, height, floor_percent,
            walkers_amount, walkers_min, walkers_max,
            spawn_chance, death_chance, turn_chance,
            enemy_amount
            ):
        self.width = width + self.SAFE_LAYER * 2
        self.height = height + self.SAFE_LAYER * 2
        self.floor_percent = floor_percent

        self.walkers_amount = walkers_amount
        self.walkers_min = walkers_min
        self.walkers_max = walkers_max
        self.spawn_chance = spawn_chance
        self.death_chance = death_chance
        self.turn_chance = turn_chance

        self.enemy_amount = enemy_amount

        self._map_data = []
        self._floor_tiles = set()

    def get_level(self):
        self._generate()
        self._spawn_objects()
        return self._map_data

    def _generate(self):
        self._map_data = [['W'] * self.width for _ in range(self.height)]
        mid_x, mid_y = self.width // 2, self.height // 2
        self._carve_floor(mid_x, mid_y)
        total_tiles = self.width * self.height
        target_floors = int(total_tiles * self.floor_percent)
        current_floors = 1
        walkers = [Walker(mid_x, mid_y) for _ in range(self.walkers_amount)]
        while current_floors < target_floors:
            walker = choice(walkers)
            walker.move()
            pos_x = int(walker.pos.x)
            pos_y = int(walker.pos.y)
            if not (self.SAFE_LAYER+1 < pos_x < self.width-self.SAFE_LAYER-2
                    and self.SAFE_LAYER+1 < pos_y < self.height-self.SAFE_LAYER-2):
                walker.bounce()
                continue
            vector = walker.vector
            extra_x = pos_x + int(vector.y)
            extra_y = pos_y + int(vector.x)
            for x, y in ((pos_x, pos_y), (extra_x, extra_y)):
                if self._map_data[y][x] == 'W':
                    self._carve_floor(x, y)
                    current_floors += 1
            if random() < self.turn_chance:
                walker.turn()
            if ((len(walkers) <= self.walkers_min
                 or random() < self.spawn_chance)
                and len(walkers) < self.walkers_max
                ):
                walkers.append(Walker(pos_x, pos_y))
            if (random() < self.death_chance
                and len(walkers) > self.walkers_min):
                walkers.remove(walker)
    
    def _carve_floor(self, x, y):
        self._map_data[y][x] = '.'
        self._floor_tiles.add((x, y))

    def _spawn_objects(self):
        _floor_tiles_amount = len(self._floor_tiles)
        positions_x, positions_y = zip(*self._floor_tiles)
        center = (
            sum(positions_x) / _floor_tiles_amount,
            sum(positions_y) / _floor_tiles_amount
        )
        most_distant = max(self._floor_tiles, key=lambda pos: dist(pos, center))
        x, y = most_distant
        OFFSET = 2
        if abs(x - center[0]) > abs(y - center[1]):
            player_pos = (x+int(copysign(OFFSET, x-center[0])), y)
        else:
            player_pos = (x, y+int(copysign(OFFSET, y-center[1])))
        for y in range(player_pos[1]-1, player_pos[1]+2):
            for x in range(player_pos[0]-1, player_pos[0]+2):
                self._carve_floor(x, y)
        self._map_data[player_pos[1]][player_pos[0]] = 'P'
        SAFE_RADIUS_TILES = (
            cfg.ENEMIES['enemy']['general']['detection_radius'] / cfg.TILE_SIZE) + 2
        enemy_pos_candidates = [
            tile_pos for tile_pos in self._floor_tiles
            if dist(tile_pos, player_pos) > SAFE_RADIUS_TILES
            ]
        if not enemy_pos_candidates: return
        actual_enemy_amount = min(self.enemy_amount, len(enemy_pos_candidates))
        enemy_positions = sample(enemy_pos_candidates, actual_enemy_amount)
        for enemy_pos in enemy_positions:
            self._map_data[enemy_pos[1]][enemy_pos[0]] = 'E'
    

class Walker:
    DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, x, y):
        self.pos = pg.Vector2(x, y)
        self.vector = pg.Vector2(choice(self.DIRECTIONS))

    def move(self):
        self.pos += self.vector

    def turn(self):
        candidates = self.DIRECTIONS.copy()
        candidates.remove(self.vector)
        self.vector.update(choice(candidates))

    def bounce(self):
        self.pos -= self.vector
        self.turn()