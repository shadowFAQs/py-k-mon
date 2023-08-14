from math import floor
import os

import pygame as pg

from area import Area
from color import BLACK, GBA_DIMS, GRAY, TRANSPARENT
from doodad import Doodad
from trainer import Trainer


def get_camera_offset(area: Area,
                      trainer_coords: tuple[float]) -> tuple[float]:
    """Center the trainer on screen without
    showing anything past the area boundaries.
    """
    screen_center = (GBA_DIMS[0] / 2, GBA_DIMS[1] / 2)
    x_from_center = pg.math.clamp(
        screen_center[0] - trainer_coords[0],
        GBA_DIMS[0] - area.dimensions()[0], 0)
    y_from_center = pg.math.clamp(
        screen_center[1] - trainer_coords[1],
        GBA_DIMS[1] - area.dimensions()[1], 0)

    return (floor(x_from_center), floor(y_from_center))


def get_dpad_input(dpad: list[bool]):
    try:
        match dpad[-1]:
            case pg.K_w:
                if not pg.K_s in dpad:
                    return 0
            case pg.K_s:
                if not pg.K_w in dpad:
                    return 1
            case pg.K_a:
                if not pg.K_d in dpad:
                    return 2
            case pg.K_d:
                if not pg.K_a in dpad:
                    return 3
    except IndexError:
        return None


def handle_keydown(dpad: list[int], key: int) -> list[int]:
    if key in [pg.K_w, pg.K_s, pg.K_a, pg.K_d]:
        dpad.append(key)

    return dpad


def handle_keyup(dpad: list[int], key: int) -> list[int]:
    if key in [pg.K_w, pg.K_s, pg.K_a, pg.K_d]:
        try:
            dpad.pop(dpad.index(key))
        except IndexError:
            dpad = []

    return dpad


def sort_entites_for_display(doodads: list[Doodad],
                             trainer: Trainer) -> list[Doodad|Trainer]:
    # Doodads are already sorted by Y value
    # TODO: Only blit entities that will be on the screen
    behind_trainer = [d for d in doodads \
        if d.grid_location.y < trainer.y_coord()]
    in_front_of_trainer = [d for d in doodads \
        if d.grid_location.y >= trainer.y_coord()]

    # Only check overlaps for nearby, valid entities
    for doodad in [d for d in doodads if d.show_in_front_of_trainer]:
        if doodad.is_nearby(trainer.grid_location):
            if doodad.colliding_with(trainer.rect):
                doodad.draw_foreground_image = True

    return behind_trainer + [trainer] + in_front_of_trainer


def update_screen(screen, small_screen, area, trainer, debug):
    screen.fill(BLACK)
    small_screen.fill(GRAY)

    camera_offset = get_camera_offset(area, trainer.center())

    area.update()
    small_screen.blit(area.image, camera_offset)

    display_list = sort_entites_for_display(area.doodads, trainer)

    for entity in display_list:
        x = entity.coords()[0] + camera_offset[0]
        y = entity.coords()[1] + camera_offset[1]
        small_screen.blit(entity.image, (x, y))

    for doodad in [d for d in area.doodads if d.draw_foreground_image]:
        doodad.draw_foreground_image = False
        x = doodad.coords()[0] + camera_offset[0]
        y = doodad.coords()[1] + camera_offset[1]
        small_screen.blit(doodad.foreground_image, (x, y))

    # frame = debug.render(f'{trainer.frame}', False, BLACK)
    # small_screen.blit(frame, (190, 20))

    pg.transform.scale(small_screen, (pg.display.get_window_size()), screen)
    pg.display.flip()


def main():
    small_screen = pg.Surface(GBA_DIMS)
    screen_dims = tuple(n * 2 for n in GBA_DIMS)
    screen = pg.display.set_mode(screen_dims)
    clock = pg.time.Clock()
    dpad = []

    area = Area('Pallet Town')
    trainer = Trainer(location=area.start_location)

    debug = pg.font.Font(os.path.join('lib', 'CompaqThin.ttf'), 12)

    running = True
    while running:
        clock.tick(30)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                dpad = handle_keydown(dpad, event.key)
            elif event.type == pg.KEYUP:
                dpad = handle_keyup(dpad, event.key)

        trainer.update(area, get_dpad_input(dpad))
        events = area.get_tile_events(trainer.grid_location)

        update_screen(screen, small_screen, area, trainer, debug)


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Pokemon FRLG Test')

    main()

    # TODO: Why are there random graphics in the lower-left corner of town??
