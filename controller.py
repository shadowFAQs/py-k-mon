import pygame as pg


class Controller():
    def __init__(self, style: str):
        self.style = style

        self.dpad = []

    def get_dpad_input(self) -> int|None:
        try:
            match self.dpad[-1]:
                case pg.K_w:
                    if not pg.K_s in self.dpad:
                        return 0
                case pg.K_s:
                    if not pg.K_w in self.dpad:
                        return 1
                case pg.K_a:
                    if not pg.K_d in self.dpad:
                        return 2
                case pg.K_d:
                    if not pg.K_a in self.dpad:
                        return 3
        except IndexError:
            return None


    def handle_keydown(self, key: int):
        if key in [pg.K_w, pg.K_s, pg.K_a, pg.K_d]:
            self.dpad.append(key)


    def handle_keyup(self, key: int):
        if key in [pg.K_w, pg.K_s, pg.K_a, pg.K_d]:
            try:
                self.dpad.pop(self.dpad.index(key))
            except IndexError:
                self.dpad = []
