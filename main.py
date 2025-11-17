import pygame as pg
from game.settings import *
from game.classes import *

pg.display.init()
pg.font.init()

display_flags = pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE
screen = pg.display.set_mode((FIRST_SCREEN_WIDTH, FIRST_SCREEN_HEIGHT), flags=display_flags, vsync=1)
game_surface = pg.Surface((GAME_WIDTH, GAME_HEIGHT))
clock = pg.time.Clock()

sprites = pg.sprite.Group()
walls = pg.sprite.Group()

def transform_surface(surface):
    cur_size = screen.get_size()
    scale_x = cur_size[0] / GAME_WIDTH
    scale_y = cur_size[1] / GAME_HEIGHT
    scale = min(scale_x, scale_y)
    scaled_width = GAME_WIDTH * scale
    scaled_height = GAME_HEIGHT * scale
    scaled_surface = pg.transform.scale(surface, (scaled_width, scaled_height))
    offset_x = (cur_size[0] - scaled_width) / 2
    offset_y = (cur_size[1] - scaled_height) / 2
    return scaled_surface, (offset_x, offset_y)

def mainloop():
    running = True
    while running:
        dt = clock.tick() / 1000

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        sprites.update(dt, walls)
        game_surface.fill((0, 0, 0))

        camera.update(player)
        for sprite in sprites:
            game_surface.blit(sprite.image, camera.adjust(sprite))

        scaled_surface, offset = transform_surface(game_surface)
        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, offset)

        player.check_dash()

        pg.display.flip()
    pg.quit()

for y, row in enumerate(WORLD_MAP):
    for x, tile in enumerate(row[::2]):
        if tile == 'W':
            wall = Wall(x, y)
            walls.add(wall)
            sprites.add(wall)
        elif tile == 'P':
            player = Player(x, y)
            sprites.add(player)
camera = Camera()

mainloop()