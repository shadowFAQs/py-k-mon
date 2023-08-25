import json
import os

import pygame as pg
from pygame.math import Vector2

from palette import TRANSPARENT
from doodad import Doodad


class Area:
    def __init__(self, name: str, start_location: tuple[int] = (0, 0)):
        self.name = name

        self.doodads        = []
        self.events         = []
        self.formatted_name = self.name.lower().replace(' ', '_')
        self.image          = None
        self.map_data       = {}
        self.passable       = None
        self.rect           = None
        self.start_location = Vector2(start_location)

        self.load_resources()

    def dimensions(self) -> tuple[int]:
        return self.image.get_size()

    def get_tile_events(self, location: Vector2, active: bool) -> list[dict]:
        events = [e for e in self.events if e['location'] == location]
        if active:
            return [e for e in events if e['type'] == 'active']
        else:
            return [e for e in events if e['type'] == 'passive']

    def is_passable(self, location: Vector2):
        if location.x < 0 or location.y < 0:  # Left/top edges of the map
            return False
        try:
            return bool(self.passable[int(location.x)][int(location.y)])
        except IndexError:
            return False

    def load_base_map(self):
        self.image = pg.image.load(
            os.path.join('lib', 'maps', f'{self.formatted_name}.png'))
        self.rect = self.image.get_rect()

    def load_doodads(self):
        self.doodads = []

        for doodad in self.map_data['doodads']:
            for location in doodad['locations']:
                self.doodads.append(Doodad(doodad['type'], location,
                                           doodad['showInFrontOfTrainer'],
                                           doodad['animated']))

        self.doodads.sort(key=lambda d: d.grid_location.y)

    def load_events(self):
        self.events = self.map_data['events']

    def load_map_data(self):
        with open(os.path.join('data', 'maps.json')) as f:
            data = json.load(f)

        self.map_data = next(
            m for m in data['areas'] if m['name'] == self.name)

    def load_resources(self):
        self.load_map_data()
        self.load_base_map()
        self.load_doodads()
        self.load_events()

        self.start_location = Vector2(self.map_data['startLocation'])

        # Boolean 2D array, such that each (x, y) is passable (1) or not (0)
        filename = f'{self.formatted_name}_passable.png'
        array = pg.surfarray.pixels2d(
            pg.image.load(os.path.join('lib', 'maps', filename)).convert(16))
        array.flat = [bool(n) for n in array.flat]
        self.passable = array

    def update(self):
        for doodad in self.doodads:
            doodad.update()
