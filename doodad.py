import pygame as pg
from pygame.math import Vector2

import os

from color import TRANSPARENT


class Doodad(pg.sprite.Sprite):
    def __init__(self, doodad_type: str, location: tuple[int],
                 show_in_front_of_trainer: bool):
        pg.sprite.Sprite.__init__(self)

        self.grid_location            = Vector2(location)
        self.show_in_front_of_trainer = show_in_front_of_trainer

        self.draw_foreground_image = False

        self.load_image(doodad_type)

    def center(self) -> tuple[float]:
        return (self.grid_location.x * 16 + self.rect.width  / 2,
                self.grid_location.y * 16 - self.rect.height / 2)

    def colliding_with(self, rect) -> bool:
        return self.rect.colliderect(rect)

    def coords(self) -> tuple[float]:
        return (self.grid_location.x * 16, self.grid_location.y * 16)

    def draw(self):
        pass

    def is_nearby(self, point: Vector2, threshold:int = 64) -> bool:
        if abs(self.grid_location.x - point.x) <= threshold:
            return abs(self.grid_location.y - point.y) <= threshold

        return False

    def load_image(self, doodad_type: str):
        self.image = pg.image.load(os.path.join(
                'lib', 'doodads', f'{doodad_type}.png')).convert(16)
        self.image.set_colorkey(TRANSPARENT)
        self.rect = self.image.get_rect()

        if self.show_in_front_of_trainer:
            self.foreground_image = pg.Surface((self.rect.width, 16))
            self.foreground_image.blit(self.image, (0, 0))
            self.foreground_image.set_colorkey(TRANSPARENT)

    def update(self):
        self.draw()
