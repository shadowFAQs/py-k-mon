import os
from string import ascii_lowercase, ascii_uppercase

import pygame as pg

from helpers import colorkeyed_surface


class Font():
    def __init__(self):
        self.image = pg.image.load(os.path.join('lib', 'menu', 'pk_font.png'))
        self.text_rows = [ascii_uppercase, ascii_lowercase,
                          '0123456789,.#!?#\'""-/##é ']

    def render_text(self, text: str) -> pg.Surface:
        letter_w, letter_h = 6, 12
        text = text.replace(':', '-')
        surface = colorkeyed_surface(
            ((letter_w + 1) * len(text), letter_h), fill=True)

        for pos, char in enumerate(text):
            letter = pg.Surface((letter_w, letter_h))
            for n, row in enumerate(self.text_rows):
                if char in row:
                    offset = -n * letter_h
                    letter.blit(self.image,
                                (row.index(char) * -letter_w, offset))
                    surface.blit(letter, (pos * (letter_w + 1), 0))

        return surface
