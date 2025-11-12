import pygame as pg
from time import perf_counter

start_time = perf_counter()

pg.display.init()
pg.font.init()

WIDTH = 900
HEIGHT = 600
FPS = 60

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption('ЫЫЫЫЫЫЫЪ')

# TODO: ...

running = True
first_frame = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # TODO: ...
    
    if first_frame:
        total_startup_time = perf_counter() - start_time
        print(f"Полное время запуска: {total_startup_time:.3f} сек")
        first_frame = False

    pg.display.flip()
    clock.tick(FPS)
pg.quit()