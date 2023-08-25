import os
from math import floor

import pygame as pg

from area import Area
from palette import BLACK, GRAY, TRANSPARENT
from controller import Controller
from dialog import Dialog
from doodad import Doodad
from trainer import Trainer


class Game():
    def __init__(self):
        self.area                   = None
        self.camera_offset          = (0, 0)
        self.clock                  = pg.time.Clock()
        self.controller             = Controller('wasd')
        self.dialog                 = None
        self.font                   = None
        self.gba_dimensions         = (240, 160)  # GB Advance screen
        self.gba_screen             = pg.Surface(self.gba_dimensions)
        self.ignore_dpad_input      = False
        self.next_A_action          = ''
        self.paused                 = True
        self.running                = True
        self.screen                 = pg.display.set_mode(
            tuple(n * 2 for n in self.gba_dimensions))
        self.state                  = 'loop'
        self.take_new_snapshot      = False
        self.target_framerate       = 30
        self.trainer                = None
        self.transition             = pg.Surface(self.gba_dimensions)
        self.transition_alpha_step  = 30
        self.transition_counter     = 0
        self.transition_max         = 20
        self.transition_snapshot    = pg.Surface(self.gba_dimensions)

        self.debug = pg.font.Font(os.path.join('lib', 'CompaqThin.ttf'), 12)

        self.load_menu_resources()

    def animate_transition(self):
        if self.state == 'fade_out':
            self.transition_counter += 1
            if self.transition_counter == self.transition_max:
                self.transition_snapshot.fill(BLACK)
                self.take_new_snapshot = True
                self.transition_snapshot.set_alpha(0)
                self.state = 'fade_in'
        elif self.state == 'fade_in':
            self.transition_counter -= 1
            if self.transition_counter == 0:
                self.state = 'loop'

    def begin_dialog(self):
        self.ignore_dpad_input = True
        events = self.area.get_tile_events(location=self.trainer.grid_location,
                                           active=True)
        event = [e for e in events if e['facing'] == self.trainer.facing][0]
        self.dialog = Dialog(event['event']['pages'], self.font)
        self.dialog.display()

    def change_map(self, new_area: str, location: tuple[int] = None,
                   fade=True):
        if fade:
            self.transition_snapshot.blit(self.gba_screen, (0, 0))

        self.area = Area(new_area)

        if self.trainer:
            if location:
                self.trainer.set_grid_location(location)
            else:
                self.trainer.set_grid_location(self.area.start_location)

    def clear_input(self):
        self.controller.clear_input()

    def do_next_A_action(self):
        if self.next_A_action:
            method = getattr(self, self.next_A_action.replace(' ', '_'))
            method()

    def draw_area(self):
        self.gba_screen.blit(self.area.image, self.camera_offset)

    def draw_doodads(self):
        for doodad in [d for d in self.area.doodads \
            if d.draw_foreground_image \
            and d.grid_location.y >= self.trainer.grid_location.y]:
            doodad.draw_foreground_image = False
            x = doodad.coords()[0] + self.camera_offset[0]
            y = doodad.coords()[1] + self.camera_offset[1]
            self.gba_screen.blit(doodad.foreground_image, (x, y))

    def execute_area_event(self, event_list: list[dict]):
        try:
            event_list = [e for e in event_list if e['type'] == 'passive']
            event = sorted(event_list, key=lambda e: e['event']['priority'])[0]
        except (IndexError, KeyError):
            return

        match event['event']['type']:
            case 'changeMap':
                self.fade_out_and_in()
                self.trainer.stop()
                self.change_map(
                    new_area=event['event']['destinationMap'],
                    location=tuple(event['event']['arrivalLocation']))

    def exit_dialog(self):
        self.state = 'loop'
        self.dialog = None
        self.ignore_dpad_input = False

    def fade_out_and_in(self, color=BLACK):
        self.state = 'fade_out'
        self.transition.fill(color)

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

    def load_menu_resources(self):
        self.font = pg.image.load(
            os.path.join('lib', 'menu', 'pk_font.png'))

    def loop(self):
        while self.running:
            self.clock.tick(self.target_framerate)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                else:
                    if self.state == 'loop':
                        if event.type == pg.KEYDOWN:
                            self.controller.handle_keydown(event.key)
                        elif event.type == pg.KEYUP:
                            self.controller.handle_keyup(event.key)

                    elif self.state == 'fade_out':
                        self.clear_input()

            self.update()
            self.animate_transition()

    def next_page(self):
        self.dialog.next_page()

    def reset_to_initial_state(self):
        self.paused = True
        self.change_map('Pallet Town', fade=False)
        self.trainer = Trainer(location=self.area.start_location)

    def set_next_A_action(self, action=''):
        if action:
            self.next_A_action = action
            return

        if self.state == 'loop':
            map_events = self.area.get_tile_events(
                location=self.trainer.grid_location, active=True)
            try:
                self.next_A_action = [e['event']['type'] \
                    for e in map_events \
                    if e['facing'] == self.trainer.facing][0]
            except IndexError:
                self.next_A_action = ''

    def skip_dialog(self):
        self.dialog.skip()

    def sort_and_draw_entities(self):
        # TODO: Only blit entities that will be on the screen
        display_list = self.sort_entites_for_display()

        for entity in display_list:
            x = entity.coords()[0] + self.camera_offset[0]
            y = entity.coords()[1] + self.camera_offset[1]
            self.gba_screen.blit(entity.image, (x, y))

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
        trainer_direction = self.controller.get_dpad_input() \
            if not self.ignore_dpad_input else None
        self.trainer.update(
            area=self.area,
            direction=trainer_direction,
            B_pressed=self.controller.is_B_down()
        )

        self.area.update()
        self.camera_offset = self.get_camera_offset()

        if self.state == 'loop':
            self.execute_area_event(
                self.area.get_tile_events(location=self.trainer.grid_location,
                                          active=False))

        if self.dialog:
            self.dialog.update()
            if self.dialog.state == 'next':
                self.set_next_A_action('next page')
            elif self.dialog.state == 'exit':
                self.set_next_A_action('exit dialog')
            else:
                self.set_next_A_action('skip dialog')
        else:
            self.set_next_A_action()

        if self.controller.A_pressed():
            self.do_next_A_action()

        self.update_screen()

        self.controller.update()

    def update_screen(self):
        self.gba_screen.fill(GRAY)

        if self.state == 'fade_out':
            self.transition.set_alpha(self.transition_alpha_step)
            self.transition_snapshot.blit(self.transition, (0, 0))
            self.gba_screen.blit(self.transition_snapshot, (0, 0))
            self.gba_screen.blit(self.transition, (0, 0))
        elif self.state == 'fade_in':
            if self.take_new_snapshot:
                self.take_new_snapshot = False
                self.draw_area()
                self.sort_and_draw_entities()
                self.draw_doodads()
                self.transition_snapshot.blit(self.gba_screen, (0, 0))

            self.transition.set_alpha(255)
            self.gba_screen.blit(self.transition, (0, 0))
            self.transition_snapshot.set_alpha(
                self.transition_snapshot.get_alpha() \
                + self.transition_alpha_step)
            self.gba_screen.blit(self.transition_snapshot, (0, 0))
        else:
            self.draw_area()
            self.sort_and_draw_entities()
            self.draw_doodads()

            text = self.debug.render(
                f'{self.trainer.grid_location}', False, BLACK)
            self.gba_screen.blit(text, (190, 20))

        if self.dialog:
            self.gba_screen.blit(self.dialog.image, self.dialog.box_offset)

        self.upsize_and_display_screen()

    def upsize_and_display_screen(self):
        self.screen.fill(GRAY)
        pg.transform.scale(self.gba_screen,
                           (pg.display.get_window_size()), self.screen)
        pg.display.flip()

    # TODO:
        # Handle player input during fade transitions (holding d-pad button starts walking once new area has loaded)
