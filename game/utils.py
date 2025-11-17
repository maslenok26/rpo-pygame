import pygame as pg
from copy import deepcopy

def scale_sprites(sprites, scale):
    for sprite in sprites:
        scaled_size = (sprite.orig_image.width*scale, sprite.orig_image.width*scale)
        sprite.image = pg.transform.scale(sprite.orig_image, scaled_size)