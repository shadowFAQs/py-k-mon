import json
import os

import pygame as pg
from pygame.math import Vector2

from color import TRANSPARENT
from doodad import Doodad


class Area:
    def __init__(self, name: str):
        self.name = name

        self.doodads        = None
        self.formatted_name = self.name.lower().replace(' ', '_')
        self.image          = None
        self.map_data       = {}
        self.passable       = None
        self.start_location = Vector2(0, 0)

        self.load_resources()

    def dimensions(self) -> tuple[int]:
        return self.image.get_size()

    def is_passable(self, location: Vector2):
        return bool(self.passable[int(location.x)][int(location.y)])

    def load_base_map(self):
        self.image = pg.image.load(
            os.path.join('lib', 'maps', f'{self.formatted_name}.png'))

    def load_doodads(self):
        self.doodads = []

        for doodad in self.map_data['doodads']:
            for location in doodad['locations']:
                self.doodads.append(Doodad(doodad['type'], location,
                                           doodad['showInFrontOfTrainer']))

        self.doodads.sort(key=lambda d: d.location.y)

    def load_map_data(self):
        with open(os.path.join('data', 'maps.json')) as f:
            data = json.load(f)

        self.map_data = next(
            m for m in data['areas'] if m['name'] == self.name)

    def load_resources(self):
        self.load_map_data()
        self.load_base_map()
        self.load_doodads()

        self.start_location = Vector2(self.map_data['startLocation'])

        # Boolean 2D array, such that each x, y
        # point is passable (1) or not (0)
        filename = f'{self.formatted_name}_passable.png'
        array = pg.surfarray.pixels2d(
            pg.image.load(os.path.join('lib', 'maps', filename)).convert(16))
        array.flat = [bool(n) for n in array.flat]  # bool(n) works here
        self.passable = array                       # because black is 0
