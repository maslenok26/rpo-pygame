from pathlib import Path

import pygame as pg

class Loader:
    def load_folder(self, path):
        folder = []
        for file in sorted(Path(path).glob('*.png')):
            image = self.load_image(file)
            folder.append(image)
        return folder

    def load_image(self, file):
        image = pg.image.load(file)
        if image.get_alpha() is not None:
            image = image.convert_alpha()
        else:
            image = image.convert()
        return image