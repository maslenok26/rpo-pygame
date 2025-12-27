import pygame as pg
from .manager import game_manager as gm
from .utils import scale_surface

def mainloop():
    fps = gm.get_fps()
    running = True
    while running:
        dt = gm.clock.tick_busy_loop(fps) / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        gm.player.update(dt, gm.collidables)
        gm.camera.update(gm.player, dt)
        gm.game_surf.fill((0, 0, 0))
        for sprite in gm.all_sprites:
            gm.game_surf.blit(sprite.image, gm.camera.adjust(sprite.rect))
        scaled_surf, offset = scale_surface(gm.screen, gm.game_surf)
        gm.screen.fill((0, 0, 0))
        gm.screen.blit(scaled_surf, offset)
        pg.display.flip()
    pg.quit()