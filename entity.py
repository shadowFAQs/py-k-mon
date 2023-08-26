import os

import pygame as pg
from pygame.math import Vector2

from palette import TRANSPARENT


class Entity(pg.sprite.Sprite):
    def __init__(self, location: Vector2, entity_name: str):
        pg.sprite.Sprite.__init__(self)

        self.grid_location  = Vector2(location)
        self.formatted_name = entity_name.lower().replace(' ', '_')

        self.action         = 'stand'
        self.actions        = ['stand']
        self.facing         = 1  # Up, Down, Left, Right
        self.frame          = 0
        self.frame_counter  = 0
        self.frame_delay    = 16
        self.grid_offset_y  = 0
        self.image          = None
        self.images         = {}
        self.rect           = None

    def advance_animation(self):
        self.frame_counter += 1
        if self.frame_counter == self.frame_delay:
            self.frame_counter = 0
            self.frame += 1

            if self.frame == len(self.images[self.action][self.facing]):
                self.frame = 0

    def center(self) -> tuple[float]:
        return self.grid_location.x * 16 + self.rect.width  / 2, \
            self.grid_location.y * 16 - self.rect.height / 2

    def coords(self) -> tuple[float]:
        return (self.grid_location.x * 16, self.grid_location.y * 16)

    def draw(self):
        self.image = self.images[self.action][self.facing][self.frame]
        self.image.set_colorkey(TRANSPARENT)
        self.rect = self.image.get_rect(
            topleft=(self.grid_location.x, self.grid_location.y + self.grid_offset_y))

        self.advance_animation()

    def is_colliding_with(self, rect) -> bool:
        return self.rect.colliderect(rect)

    def is_nearby(self, point: Vector2, threshold:int = 96) -> bool:
        if abs(self.grid_location.x - point.x) <= threshold:
            return abs(self.grid_location.y - point.y) <= threshold

        return False

    def load_sheet(self, entity_type: str, sheet_name: str, sheet_width: int,
                   flip: bool) -> list[pg.Surface]:
        frames = []
        sheet = pg.image.load(
            os.path.join('lib', entity_type, sheet_name))

        for n in range(sheet.get_width() // sheet_width):
            frame = pg.Surface((sheet_width, sheet.get_height()))
            frame.blit(sheet, (-n * sheet_width, 0))
            if flip:
                frame = pg.transform.flip(frame, True, False)
            frames.append(frame)

        return frames

    def update(self):
        self.advance_animation()
        self.draw()
