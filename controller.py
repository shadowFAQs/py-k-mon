import pygame as pg


class Button():
    def __init__(self, name: str, binding: int, dpad: bool=False):
        self.binding = binding
        self.dpad    = dpad
        self.name    = name

        self.flag    = False  # Fires once on press
        self.is_down = False

    def as_int(self) -> int:
        if not self.dpad:
            raise RuntimeError(
                f'Button "{self.name}" cannot be interpreted as an int')
        return ['UP', 'DOWN', 'LEFT', 'RIGHT'].index(self.name)

    def press(self):
        self.flag = True
        self.is_down = True

    def release(self):
        self.flag = False
        self.is_down = False

    def update(self):
        self.flag = False


class Controller():
    def __init__(self, style: str):
        self.style = style  # WASD, arrows

        self.buttons = []
        self.set_buttons_from_style()

    def button(self, name: str) -> Button:
        return next(b for b in self.buttons if b.name == name)

    def get_dpad(self) -> list[Button]:
        return [b for b in self.buttons if b.dpad]

    def get_dpad_input(self) -> int|None:
        try:
            return next(b for b in self.get_dpad() if b.is_down).as_int()
        except StopIteration:
            return None

    def get_flags(self) -> list[Button]:
        return [b for b in self.buttons if b.flag]

    def get_pressed(self) -> list[Button]:
        return [b for b in self.buttons if b.is_down]

    def handle_keydown(self, key: int):
        try:
            button = next(b for b in self.buttons if b.binding == key)
            button.press()
        except StopIteration:
            pass

    def handle_keyup(self, key: int):
        try:
            button = next(b for b in self.buttons if b.binding == key)
            button.release()
        except StopIteration:
            pass

    def poll(self):
        """Manually poll controller keys"""
        for button in self.buttons:
            if pg.key.get_pressed()[button.binding]:
                button.is_down = True

    def reset(self):
        for btn in self.buttons:
            btn.release()

    def set_buttons_from_style(self):
        match self.style:
            case 'wasd':
                buttons = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                bindings = [pg.K_w, pg.K_s, pg.K_a, pg.K_d]
                for n in range(len(buttons)):
                    self.buttons.append(Button(
                        name=buttons[n], binding=bindings[n], dpad=True))

                buttons = ['A', 'B', 'START']
                bindings = [pg.K_u, pg.K_h, pg.K_SPACE]
                for n in range(len(buttons)):
                    self.buttons.append(Button(
                        name=buttons[n], binding=bindings[n]))

    def update(self):
        for button in self.buttons:
            button.update()
