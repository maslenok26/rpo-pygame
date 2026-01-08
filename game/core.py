import pygame as pg

from .manager import GameManager


def mainloop(gm: GameManager):

    pg.mouse.set_pos(gm.screen.width // 1.453, gm.screen.height // 2)
    fps = gm.get_fps()
    running = True

    while running:
        dt = gm.clock.tick_busy_loop(fps) / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.VIDEORESIZE:
                gm.update_layout()
        gm.update(dt)
        gm.draw()
        pg.display.flip()

    pg.quit()