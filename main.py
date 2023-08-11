import os

import pygame as pg

from area import Area
from color import BLACK, GBA_DIMS, GRAY, TRANSPARENT
from trainer import Trainer


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


def update_screen(screen, small_screen, area, trainer, debug):
    screen.fill(BLACK)
    small_screen.fill(GRAY)

    small_screen.blit(area.image, (0, 0))

    for entity in [trainer]:
        small_screen.blit(entity.image, entity.coords() + area.offset)

    location = debug.render(
        f'{trainer.location.x}, {trainer.location.y}', False, BLACK)

    small_screen.blit(location, (180, 20))

    pg.transform.scale(small_screen, (pg.display.get_window_size()), screen)
    pg.display.flip()


def main():
    small_screen = pg.Surface(GBA_DIMS)
    screen_dims = tuple(n * 2 for n in GBA_DIMS)
    screen = pg.display.set_mode(screen_dims)
    clock = pg.time.Clock()
    dpad = []

    area = Area('Pallet Town')
    trainer = Trainer(location=(6, 8))

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

        update_screen(screen, small_screen, area, trainer, debug)


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Pokemon FRLG Test')

    main()
