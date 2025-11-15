import pygame as pg
from time import perf_counter
from game.settings import WIDTH, HEIGHT, WORLD_MAP
from game.classes import *

start_time = perf_counter()

pg.display.init()
pg.font.init()

display_flags = pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE
screen = pg.display.set_mode((WIDTH, HEIGHT), flags=display_flags, vsync=1)
clock = pg.time.Clock()
pg.display.set_caption('ЫЫЫЫЫЫЫЪ')

sprites = pg.sprite.Group()
walls = pg.sprite.Group()

for y, row in enumerate(WORLD_MAP):
    for x, tile in enumerate(row[::2]):
        if tile == 'W':
            wall = Wall(x, y)
            walls.add(wall)
            sprites.add(wall)
        elif tile == 'P':
            player = Player(x, y)
            sprites.add(player)

running = True
first_frame = True
while running:
    dt = clock.tick() / 1000
    print(1/dt)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    if first_frame:
        total_startup_time = perf_counter() - start_time
        print(f"Время запуска: {total_startup_time:.3f} сек")
        first_frame = False

    sprites.update(dt, walls)
    screen.fill((0, 0, 0))
    sprites.draw(screen)

    pg.display.flip()
pg.quit()