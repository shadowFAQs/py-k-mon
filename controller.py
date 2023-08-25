import pygame as pg


class Controller():
    def __init__(self, style: str):
        self.style = style  # WASD, arrows

        self.A_flag  = False  # These flags are for capturing initial
        self.B_flag  = False  # presses only.
        self.buttons = []
        self.dpad    = []

    def A_pressed(self) -> bool:
        return self.A_flag

    def clear_buttons(self):
        self.buttons = []
        self.A_flag = False
        self.B_flag = False

    def clear_input(self):
        self.dpad = []
        self.clear_buttons()

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
        elif key in [pg.K_u, pg.K_h, pg.K_SPACE]:
            self.buttons.append(key)

            match key:
                case pg.K_u:
                    self.A_flag = True
                case pg.K_h:
                    self.B_flag = True

    def handle_keyup(self, key: int):
        if key in [pg.K_w, pg.K_s, pg.K_a, pg.K_d]:
            try:
                self.dpad.pop(self.dpad.index(key))
            except ValueError:
                self.dpad = []
        if key in [pg.K_u, pg.K_h, pg.K_SPACE]:
            try:
                self.buttons.pop(self.buttons.index(key))
            except ValueError:
                self.clear_buttons()

    def is_A_down(self) -> bool:
        return pg.K_u in self.buttons

    def is_B_down(self) -> bool:
        return pg.K_h in self.buttons

    def poll(self):
        """Manually poll controller keys"""
        # Dpad
        for key in [pg.K_w, pg.K_s, pg.K_a, pg.K_d]:
            if pg.key.get_pressed()[key]:
                self.dpad.append(key)
        # Buttons
        for key in [pg.K_u, pg.K_h, pg.K_SPACE]:
            if pg.key.get_pressed()[key]:
                self.buttons.append(key)

    def update(self):
        self.A_flag = False
        self.B_flag = False
