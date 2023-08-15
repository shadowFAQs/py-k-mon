import os
from math import floor

import pygame as pg

from area import Area
from palette import BLACK, TRANSPARENT
from controller import Controller
from doodad import Doodad
from trainer import Trainer


class Game():
    def __init__(self):
        self.area           = None
        self.camera_offset  = (0, 0)
        self.clock          = pg.time.Clock()
        self.controller     = Controller('wasd')
        self.gba_dimensions = (240, 160)  # GB Advance screen dimensions
        self.gba_screen     = pg.Surface(self.gba_dimensions)
        self.paused         = True
        self.running        = True
        self.screen         = pg.display.set_mode(
            tuple(n * 2 for n in self.gba_dimensions))
        self.trainer        = None

        self.debug = pg.font.Font(os.path.join('lib', 'CompaqThin.ttf'), 12)

    def change_map(self, new_area: str, location: tuple[int] = None):
        # TODO: Animate transition

        if location:
            self.area = Area(new_area, location)
        else:
            self.area = Area(new_area)

        if self.trainer:
            self.trainer.grid_location = self.area.start_location

    def execute_area_event(self, event_list: list[dict]):
        try:
            event = sorted(event_list, key=lambda e: e['event']['priority'])[0]
        except IndexError:
            return

        match event['event']['type']:
            case 'changeMap':
                self.trainer.stop()
                self.change_map(
                    new_area=event['event']['destinationMap'],
                    location=tuple(event['event']['arrivalLocation']))

    def get_camera_offset(self) -> tuple[float]:
        """Center the trainer on screen without
        showing anything past the area boundaries.
        """

        screen_center = tuple(d / 2 for d in self.gba_dimensions)

        if self.area.rect.w <= self.gba_dimensions[0]:
            x_from_center = (self.gba_dimensions[0] - self.area.rect.w) / 2
        else:
            x_from_center = pg.math.clamp(
            screen_center[0] - self.trainer.center()[0],
            self.gba_dimensions[0] - self.area.dimensions()[0], 0)

        if self.area.rect.h <= self.gba_dimensions[1]:
            y_from_center = (self.gba_dimensions[1] - self.area.rect.h) / 2
        else:
            y_from_center = pg.math.clamp(
            screen_center[1] - self.trainer.center()[1],
            self.gba_dimensions[1] - self.area.dimensions()[1], 0)

        return (floor(x_from_center), floor(y_from_center))

    def loop(self):
        while self.running:
            self.clock.tick(30)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    self.controller.handle_keydown(event.key)
                elif event.type == pg.KEYUP:
                    self.controller.handle_keyup(event.key)

            self.update()

    def reset_to_initial_state(self):
        self.paused = True
        self.change_map('Pallet Town')
        self.trainer = Trainer(location=self.area.start_location)

    def sort_entites_for_display(self) -> list[Doodad|Trainer]:
        # Doodads are already sorted by Y value
        behind_trainer = [d for d in self.area.doodads \
            if d.grid_location.y <= self.trainer.grid_location.y]
        in_front_of_trainer = [d for d in self.area.doodads \
            if d.grid_location.y > self.trainer.grid_location.y]

        # Only check overlaps for nearby, valid entities
        for doodad in [d for d in self.area.doodads \
            if d.show_in_front_of_trainer]:
            if doodad.is_nearby(self.trainer.grid_location):
                if doodad.is_colliding_with(self.trainer.rect):
                    doodad.draw_foreground_image = True

        return behind_trainer + [self.trainer] + in_front_of_trainer

    def update(self):
        self.trainer.update(
            area=self.area,
            direction=self.controller.get_dpad_input())

        self.area.update()
        self.camera_offset = self.get_camera_offset()

        self.execute_area_event(
            self.area.get_tile_events(self.trainer.grid_location))

        self.update_screen()

    def update_screen(self):
        self.screen.fill(BLACK)
        self.gba_screen.fill(BLACK)
        self.gba_screen.blit(self.area.image, self.camera_offset)

        display_list = self.sort_entites_for_display()

        for entity in display_list:
            x = entity.coords()[0] + self.camera_offset[0]
            y = entity.coords()[1] + self.camera_offset[1]
            self.gba_screen.blit(entity.image, (x, y))

        for doodad in [d for d in self.area.doodads \
            if d.draw_foreground_image \
            and d.grid_location.y >= self.trainer.grid_location.y]:
            doodad.draw_foreground_image = False
            x = doodad.coords()[0] + self.camera_offset[0]
            y = doodad.coords()[1] + self.camera_offset[1]
            self.gba_screen.blit(doodad.foreground_image, (x, y))

        # text = self.debug.render(f'{fits_on_screen}', False, BLACK)
        # self.gba_screen.blit(text, (190, 20))

        pg.transform.scale(
            self.gba_screen, (pg.display.get_window_size()), self.screen)
        pg.display.flip()
