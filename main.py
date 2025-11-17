import pygame as pg
from game.settings import *
from game.classes import *
from game.utils import *

pg.display.init()

display_flags = pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE
screen = pg.display.set_mode((FIRST_SCREEN_WIDTH, FIRST_SCREEN_HEIGHT), flags=display_flags, vsync=1)
game_surf = pg.Surface((GAME_WIDTH, GAME_HEIGHT))
clock = pg.time.Clock()

sprites = pg.sprite.Group()
walls = pg.sprite.Group()

def mainloop():
    running = True
    while running:
        dt = clock.tick() / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        player.get_input()
        player.update(dt, walls)
        camera.update(player, dt)
        game_surf.fill((0, 0, 0))
        for sprite in sprites:
            game_surf.blit(sprite.image, camera.adjust(sprite))
        scaled_surf, offset = transform_surface(screen, game_surf)
        screen.fill((0, 0, 0))
        screen.blit(scaled_surf, offset)
        player.check_dash()
        pg.display.flip()
    pg.quit()

for y, row in enumerate(WORLD_MAP):
    for x, tile in enumerate(row.split()):
        if tile == 'W':
            wall = Wall(x, y, (sprites, walls))
        elif tile == 'P':
            player = Player(x, y, (sprites))
camera = Camera()

mainloop()