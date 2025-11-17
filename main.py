import pygame as pg
from game.settings import *
from game.classes import *
from game.utils import *

pg.display.init()
pg.font.init()

screen_size = (FIRST_SCREEN_WIDTH, FIRST_SCREEN_HEIGHT)
display_flags = pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE
screen = pg.display.set_mode(screen_size, flags=display_flags, vsync=1)
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
    scale = FIRST_SCALE
    running = True
    while running:
        dt = clock.tick() / 1000

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.VIDEORESIZE:
                scale = min(screen.height/GAME_WIDTH, screen.height/GAME_HEIGHT)
                scale_sprites(sprites, scale)

        sprites.update(dt, walls)
        screen.fill((0, 0, 0))

        camera.update(player)
        for sprite in sprites:
            screen.blit(sprite.image, camera.get_render_pos(sprite, scale))
        
        # scaled_surface, offset = scale_surface(game_surface)
        # screen.fill((0, 0, 0))
        # screen.blit(scaled_surface, offset)

        player.check_dash()

        pg.display.flip()
    pg.quit()

for y, row in enumerate(WORLD_MAP):
    for x, tile in enumerate(row.split()):
        if tile == 'W':
            wall = Wall(x, y)
            walls.add(wall)
            sprites.add(wall)
        elif tile == 'P':
            player = Player(x, y)
            sprites.add(player)
camera = Camera()

scale_sprites(sprites, FIRST_SCALE)
mainloop()