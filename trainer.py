import os

import pygame as pg
from pygame.math import Vector2

from color import TRANSPARENT


class Trainer(pg.sprite.Sprite):
    def __init__(self, location: Vector2):
        pg.sprite.Sprite.__init__(self)

        self.grid_location = location

        self.action          = 'stand'
        self.facing          = 1  # Up, Down, Left, Right
        self.frame           = 0
        self.frame_delay     = 15
        self.frame_counter   = 0
        self.image           = None
        self.images          = None
        self.input_counter   = 0
        self.input_delay     = 3
        self.rect            = None
        self.target_location = self.grid_location
        self.walk_speed      = 0.1

        self.load_images('trainer')

    def advance_animation(self):
        self.frame_counter += 1
        if self.frame_counter == self.frame_delay:
            self.frame_delay = 0
            self.frame_counter = 0
            self.frame += 1

            if self.frame == len(self.images[self.action][self.facing]):
                self.frame = 0

    def center(self) -> tuple[float]:
        # Y - 1 because trainer sprite is 2 tiles tall
        return (self.grid_location.x * 16 + self.rect.width  / 2,
                (self.grid_location.y - 1) * 16 - self.rect.height / 2)

    def coords(self) -> tuple[float]:
        return (self.grid_location.x * 16, (self.grid_location.y - 1) * 16)

    def draw(self):
        if self.action == 'walk':
            self.grid_location.move_towards_ip(
                self.target_location, self.walk_speed)

        self.image = self.images[self.action][self.facing][self.frame]
        self.image.set_colorkey(TRANSPARENT)
        self.rect = self.image.get_rect(
            topleft=(self.grid_location.x, self.grid_location.y))

        self.advance_animation()

    def load_images(self, base_filepath: str):
        stand_up = pg.image.load(
            os.path.join('lib', f'{base_filepath}_up.png')).convert(16)
        stand_down = pg.image.load(
            os.path.join('lib', f'{base_filepath}_down.png')).convert(16)
        stand_left = pg.image.load(
            os.path.join('lib', f'{base_filepath}_left.png')).convert(16)
        stand_right = pg.transform.flip(stand_left, True, False)

        self.images = {
            'stand': [[stand_up], [stand_down], [stand_left], [stand_right]],
            'walk': [[stand_up], [stand_down], [stand_left], [stand_right]]
        }

    def move(self, area):
        self.action = 'walk'

        match self.facing:
            case 0:
                target = self.grid_location + Vector2(0, -1)
            case 1:
                target = self.grid_location + Vector2(0, 1)
            case 2:
                target = self.grid_location + Vector2(-1, 0)
            case 3:
                target = self.grid_location + Vector2(1, 0)

        if area.is_passable(target):
            self.target_location = target
        else:
            self.target_location = self.grid_location

    def set_action_from_input(self, area, direction):
        if self.action == 'stand':
            if direction is None:
                self.stop()
            else:
                self.facing = direction

                self.input_counter += 1
                if self.input_counter == self.input_delay:
                    self.move(area)

        elif self.action == 'walk':
            if self.grid_location == self.target_location:
                if direction is None:
                    self.stop()
                else:
                    self.facing = direction
                    self.move(area)

    def snap_location_to_grid(self):
        '''Vector2.move_towards_ip will never
        actually "complete" moving one vector to
        the position of another, so this method
        snaps the location there when it's close
        enough.
        '''
        if abs(self.grid_location.x - self.target_location.x) <= 0.1:
            self.grid_location.x = self.target_location.x
        if abs(self.grid_location.y - self.target_location.y) <= 0.1:
            self.grid_location.y = self.target_location.y

    def stop(self):
        self.action = 'stand'
        self.input_counter = 0
        self.target_location = self.grid_location

    def update(self, area, direction=None):
        self.snap_location_to_grid()
        self.set_action_from_input(area, direction)

        self.draw()
