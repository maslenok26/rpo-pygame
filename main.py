import pygame as pg
from game.settings import *
from game.classes import *
from game.utils import scale_surface

pg.display.init()

display_flags = pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE
screen = pg.display.set_mode(
    (START_SCREEN_WIDTH, START_SCREEN_HEIGHT), flags=display_flags, vsync=1
    )
game_surf = pg.Surface((GAME_WIDTH, GAME_HEIGHT))
clock = pg.time.Clock()

sprites: pg.sprite.Group[pg.sprite.Sprite] = pg.sprite.Group()
collidables: pg.sprite.Group[pg.sprite.Sprite] = pg.sprite.Group()

for y, row in enumerate(WORLD_MAP):
    for x, tile in enumerate(row.split()):
        if tile == 'W':
            wall = Wall(x, y, (sprites, collidables))
        elif tile == 'P':
            player = Player(x, y, (sprites))
camera = Camera()

def mainloop():
    fps = FPS if FPS_LOCK else 0
    running = True
    while running:
        dt = clock.tick_busy_loop(fps) / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        player.update(dt, collidables)
        camera.update(player, dt)
        game_surf.fill((0, 0, 0))
        for sprite in sprites:
            game_surf.blit(sprite.image, camera.adjust(sprite.rect))
        scaled_surf, offset = scale_surface(screen, game_surf)
        screen.fill((0, 0, 0))
        screen.blit(scaled_surf, offset)
    
        pg.display.flip()
    pg.quit()

mainloop()