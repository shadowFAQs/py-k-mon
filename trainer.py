import os

import pygame as pg
from pygame.math import Vector2

from area import Area
from palette import TRANSPARENT
from entity import Entity


class Trainer(Entity):
    def __init__(self, location: Vector2):
        # Entity is instanciated with a Y offset
        # of -1 because unit sprites are 2 tiles
        # tall but "stand" on the lower one.
        super().__init__(location, 'trainer')

        self.actions         = ['stand', 'run', 'walk']
        self.entity_type     = 'unit'
        self.frame_delay     = 7   # Override
        self.grid_offset_y   = -1  # Override
        self.input_counter   = 0
        self.input_delay     = 3
        self.target_location = self.grid_location
        self.walk_speed      = 0.1

        self.load_images()
        self.draw()

    def coords(self) -> tuple[float]:
        x, y = super().coords()
        return x, y + self.grid_offset_y * 16

    def draw(self):
        if self.action == 'walk':
            self.frame_delay = 7
            self.grid_location.move_towards_ip(
                self.target_location, self.walk_speed)
        elif self.action == 'run':
            self.frame_delay = 4
            self.grid_location.move_towards_ip(
                self.target_location, self.walk_speed * 2)

        super().draw()

    def load_images(self):
        for action in self.actions:
            self.images[action] = [
                self.load_sheet(
                    entity_type=self.entity_type,
                    sheet_name=f'{self.formatted_name}_{action}_up.png',
                    sheet_width=16,
                    flip=False
                ),
                self.load_sheet(
                    entity_type=self.entity_type,
                    sheet_name=f'{self.formatted_name}_{action}_down.png',
                    sheet_width=16,
                    flip=False
                ),
                self.load_sheet(
                    entity_type=self.entity_type,
                    sheet_name=f'{self.formatted_name}_{action}_left.png',
                    sheet_width=16,
                    flip=False
                ),
                self.load_sheet(
                    entity_type=self.entity_type,
                    sheet_name=f'{self.formatted_name}_{action}_left.png',
                    sheet_width=16,
                    flip=True
                )]

    def move(self, area: Area, B_pressed: bool):
        self.set_action('run' if B_pressed else 'walk')

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

    def set_action(self, action: str):
        self.frame_counter = 0
        self.action = action

    def set_action_from_input(self, area: Area, direction: int|None,
                              B_pressed: bool):
        if self.action == 'stand':
            if direction is None:
                self.stop()
            else:
                self.facing = direction

                self.input_counter += 1
                if self.input_counter == self.input_delay:
                    self.move(area, B_pressed)

        elif self.action in ['run', 'walk']:
            if self.grid_location == self.target_location:
                if direction is None:
                    self.stop()
                else:
                    self.facing = direction
                    self.move(area, B_pressed)

    def set_grid_location(self, location: tuple[int] | Vector2):
        self.grid_location = Vector2(location)

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
        self.frame_counter = 0
        self.frame = 0
        self.input_counter = 0
        self.target_location = self.grid_location

    def update(self, area: Area, direction=None, B_pressed=False):
        self.snap_location_to_grid()
        self.set_action_from_input(area, direction, B_pressed)
        super().advance_animation()
        self.draw()
