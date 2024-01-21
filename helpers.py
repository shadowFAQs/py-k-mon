import os

import pygame as pg

from palette import TRANSPARENT


def colorkeyed_surface(dimensions: tuple[int], fill: bool=False) -> pg.Surface:
    surface = pg.Surface(dimensions)
    surface.set_colorkey(TRANSPARENT)
    if fill:
        surface.fill(TRANSPARENT)
    return surface


def colorkeyed_surface_from_file(*filepath_parts: str, fill: bool=False) -> pg.Surface:
    surface = pg.image.load(os.path.join(*filepath_parts))
    surface.set_colorkey(TRANSPARENT)
    if fill:
        surface.fill(TRANSPARENT)
    return surface


def increment_with_wrap(value: int, increment: int, max_value: int) -> int:
    value += increment
    if value < 0:
        return max_value
    if value > max_value:
        return 0
    return value
