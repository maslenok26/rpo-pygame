import pygame as pg
from game.settings import *
from game.classes import *
from game.utils import scale_surface
from game.core import mainloop
from game.manager import game_manager as gm

width, height = gm.screen.get_size()
pg.mouse.set_pos(width // 2, height // 2)

if __name__ == '__main__':
    mainloop()