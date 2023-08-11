import os

import pygame as pg
from pygame.math import Vector2


class Area:
    def __init__(self, name: str):
        self.name = name

        self.image    = None
        self.offset   = Vector2(1, -4)
        self.passable = None

        self.load_resources()

    def is_passable(self, location: Vector2):
        return bool(self.passable[int(location.x)][int(location.y)])

    def load_resources(self):
        formatted_name = self.name.lower().replace(' ', '_')
        self.image = pg.image.load(
            os.path.join('lib', f'{formatted_name}.png'))

        # Boolean 2D array, such that each x, y
        # point is passable (1) or not (0)
        filename = f'{formatted_name}_passable.png'
        array = pg.surfarray.pixels2d(
            pg.image.load(os.path.join('lib', filename)).convert(16))
        array.flat = [bool(n) for n in array.flat]
        self.passable = array
