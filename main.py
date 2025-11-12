import pygame as pg
from time import perf_counter

start_time = perf_counter()

pg.display.init()
pg.font.init()

WIDTH = 900
HEIGHT = 600
FPS = 60
dt = 0

display_flags = pg.HWSURFACE | pg.DOUBLEBUF
screen = pg.display.set_mode((WIDTH, HEIGHT), display_flags)
clock = pg.time.Clock()
pg.display.set_caption('ЫЫЫЫЫЫЫЪ')

# TODO: ...

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 50))
        self.image.fill((150, 255, 150))
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.speed = 300
        self.vector = pg.math.Vector2(0, 0)
        self.pos = pg.math.Vector2(self.rect.center)
    
    def get_input(self):
        self.vector.x, self.vector.y = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vector.y -= 1
        if keys[pg.K_a]:
            self.vector.x -= 1
        if keys[pg.K_s]:
            self.vector.y += 1
        if keys[pg.K_d]:
            self.vector.x += 1
        if self.vector.length() != 0:
            self.vector = self.vector.normalize()

    def move(self, dt):
        self.pos += self.vector * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def update(self, dt):
        self.get_input()
        self.move(dt)

sprites = pg.sprite.Group()
player = Player()
sprites.add(player)
running = True
first_frame = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    if first_frame:
        total_startup_time = perf_counter() - start_time
        print(f"Время запуска: {total_startup_time:.3f} сек")
        first_frame = False

    # TODO: ...
    
    sprites.update(dt)
    screen.fill((0, 0, 0))
    sprites.draw(screen)

    pg.display.flip()
    dt = clock.tick(FPS) / 1000
pg.quit()