import pygame as pg
from game.core import mainloop
from game.manager import GameManager

pg.display.init()

if __name__ == '__main__':
    game_manager = GameManager()
    mainloop(game_manager)