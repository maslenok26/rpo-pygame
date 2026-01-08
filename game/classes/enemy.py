from .entity import Entity
from ..settings import LAYERS, TILE_SIZE
from ..utils import scale_image


class Enemy(Entity):
    def __init__(self, sprite_groups, x, y):
        super().__init__(sprite_groups)

        self._layer = LAYERS['PLAYER']
        self.add_to_groups('rendering', 'hittables', 'enemies')

        self.hp = 100
        self.damage = 10
        self.speed = TILE_SIZE

        self.image = scale_image('enemy.png', (14, 14))
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))

        self._init_hitbox(10, 10, self.rect.center)

        self.target = None

    def update(self):
        self._follow_target()
        
    def _follow_target(self):
        pass