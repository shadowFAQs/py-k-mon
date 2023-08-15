import pygame as pg
from pygame.math import Vector2

import os

from palette import BLACK, TRANSPARENT
from entity import Entity


class Doodad(Entity):
    def __init__(self, doodad_type: str, location: tuple[int],
                 show_in_front_of_trainer: bool, animated: bool):
        super().__init__(location, doodad_type)

        self.show_in_front_of_trainer = show_in_front_of_trainer
        self.animated = animated

        self.draw_foreground_image    = False
        self.entity_type              = 'doodad'
        self.foreground_image         = None

        self.load_images()
        self.draw()
        self.set_foreground_image()

    def __repr__(self):
        return f'{self.formatted_name.replace("_", " ")} @ {self.grid_location}'

    def load_images(self):
        image = pg.image.load(
            os.path.join('lib', self.entity_type,
                         f'{self.formatted_name}.png'))
        sheet_width = 16 if self.animated else image.get_width()
        base = self.load_sheet(
            entity_type=self.entity_type,
            sheet_name=f'{self.formatted_name}.png',
            sheet_width=sheet_width,
            flip=False
        )
        self.images['stand'] = [base] * 4

    def set_foreground_image(self):
        if self.show_in_front_of_trainer:
            self.foreground_image = pg.Surface((self.rect.width, 32))
            self.foreground_image.blit(self.image, (0, 0))
            self.foreground_image.set_colorkey(BLACK)
