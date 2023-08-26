import os

import pygame as pg

from helpers import colorkeyed_surface, colorkeyed_surface_from_file
from palette import TRANSPARENT

class Dialog():
    def __init__(self, pages, font):
        self.font            = font
        self.letter_h        = 12
        self.letter_w        = 6
        self.pages           = pages

        self.box             = None
        self.box_offset      = (5, 106)
        self.chars_offset    = (13, 10)
        self.chars_per_line  = 29
        self.continue_button = None
        self.frame_counter   = 0
        self.image           = None
        self.letter          = 0
        self.letter_objs     = []
        self.frame_max       = 2
        self.page            = 0
        self.state           = 'spawn'

        self.load_resources()

    def animate(self):
        if self.state == 'typewriter':
            if not self.letter_objs:
                self.letter_objs = self.render_dialog_text(
                    self.pages[self.page])
                self.image.fill(TRANSPARENT)
                self.image.blit(self.box, (0, 0))

            self.frame_counter += 1
            if self.frame_counter == self.frame_max:
                self.frame_counter = 0
                self.letter += 1

            if self.letter == len(self.pages[self.page]):
                self.set_next_state()
            else:
                self.blit_next_letter()

    def blit_next_letter(self):
        try:
            letter = self.letter_objs[self.letter]
            self.image.blit(
                letter['surface'],
                (self.chars_offset[0] + letter['x'],
                 letter['y'] + self.chars_offset[1])
            )
        except IndexError:
            pass

    def display(self):
        self.state = 'typewriter'

    def load_resources(self):
        self.box = colorkeyed_surface_from_file('lib', 'menu', 'dialog.png')
        self.continue_button = colorkeyed_surface_from_file(
            'lib', 'menu', 'continue_button.png')
        self.image = colorkeyed_surface(self.box.get_size(), fill=True)

    def next_page(self):
        self.letter = 0
        self.page += 1
        self.letter_objs = []
        self.state = 'typewriter'

    def render_dialog_text(self, text: str) -> dict:
        words = text.replace(':', '-').split(' ')
        line0 = []
        line_length_exceeded = False
        while words and not line_length_exceeded:
            line0.append(words.pop(0))
            if words:
                line_length_exceeded = len(' '.join(line0 + [words[0]])) \
                    > self.chars_per_line

        letters = []
        for l, line in enumerate([line0, words]):
            current_pos = 0

            for char in ' '.join(line):
                letter = {
                    'surface': colorkeyed_surface(
                        (self.letter_w, self.letter_h))
                }

                for n, row in enumerate(self.font.text_rows):
                    if char in row:
                        offset = -n * self.letter_h
                        letter['surface'].blit(
                            self.font.image,
                            (row.index(char) * -self.letter_w, offset)
                        )
                        letter['x'] = current_pos * (self.letter_w + 1)
                        letter['y'] = l * self.letter_h
                        letters.append(letter)
                        break

                current_pos += 1

        return letters

    def set_next_state(self):
        self.frame_counter = 0

        if self.page < len(self.pages) - 1:
            self.state = 'next'
        else:
            self.state = 'exit'

    def skip(self):
        while self.letter < len(self.pages[self.page]):
            self.letter += 1
            self.blit_next_letter()

        self.set_next_state()

    def update(self):
        if self.state == 'next':
            # Place "continue" button
            self.image.blit(self.continue_button,
                (self.letter_objs[-1]['x'] + self.chars_offset[0] + 12,
                 self.letter_objs[-1]['y'] + self.chars_offset[1]))

        self.animate()

