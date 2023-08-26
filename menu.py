import pygame as pg
from pygame.math import Vector2

from controller import Button
from font import Font
from helpers import colorkeyed_surface, colorkeyed_surface_from_file, \
                    increment_with_wrap
from palette import TRANSPARENT


class Menu(pg.sprite.Sprite):
    def __init__(self):
        self.background      = None
        self.coords          = Vector2(0, 0)
        self.cursor          = None
        self.cursor_offset   = (0, 0)
        self.cursor_position = 0
        self.cursor_type     = ''
        self.font            = Font()
        self.items           = []
        self.name            = ''
        self.open            = False
        self.row_height      = 0
        self.text_offset     = (0, 0)

    def back(self, arg):
        print('Menu.back()')

    def close(self, arg):
        if self.open:  # Prevent immediate firing when menu is first opened
            print('Menu.close()')

    def draw(self):
        self.image.fill(TRANSPARENT)
        self.image.blit(self.background, (0, 0))

        for item in self.items:
            self.image.blit(item['image'], item['coords'])

        self.image.blit(self.cursor, self.get_cursor_coords())

    def get_action_from_input(self, buttons: list[Button]) -> tuple:
        if not buttons:
            return None, ''

        match buttons[-1].name:
            case 'START':
                return self.close, ''
            case 'A':
                return self.select, ''
            case 'B':
                return self.back, ''
            case 'UP':
                return self.navigate, 'up'
            case 'DOWN':
                return self.navigate, 'down'
            case _:
                return None, ''

    def get_cursor_coords(self) -> tuple[int]:
        return (self.cursor_offset[0],
                self.cursor_offset[1] + self.cursor_position * self.row_height)

    def load_images(self):
        self.background = colorkeyed_surface_from_file(
            'lib', 'menu', f'{self.name}.png')
        self.image = colorkeyed_surface(self.background.get_size(), fill=True)

        if self.cursor_type:
            self.cursor = colorkeyed_surface_from_file(
                'lib', 'menu', f'{self.cursor_type}_cursor.png')

    def navigate(self, direction: str):
        match direction:
            case 'up':
                mod = -1
            case 'down':
                mod = 1
            case _:
                return

        self.cursor_position = increment_with_wrap(
            value=self.cursor_position,
            increment=mod,
            max_value=len(self.items) - 1
        )

    def select(self, arg):
        print('Menu.select()')

    def update(self):
        if not self.open:     # Prevent immediate firing of close() when menu
            self.open = True  # is first opened

        self.draw()


class Overworld_Sidebar(Menu):
    def __init__(self):
        super().__init__()

        self.name            = 'overworld_sidebar'
        self.coords          = (159, 1)
        self.cursor_type     = 'row'
        self.cursor_offset   = (8, 8)
        self.row_height      = 14
        self.text_offset     = (8, 14)

        super().load_images()
        self.set_items()

    def set_items(self):
        for row, item in enumerate(['POKéDEX', 'POKéMON', 'BAG', 'ASH', 'SAVE',
                                    'OPTION', 'EXIT']):
            self.items.append(
                dict(
                    image=self.font.render_text(item),
                    coords=(self.text_offset[0] + self.cursor_offset[0],
                            self.text_offset[1] * row + self.cursor_offset[1])
                )
            )
