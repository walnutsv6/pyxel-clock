import pyxel
import datetime
from face import draw_face
from hands import draw_hands

CX, CY, R = 72, 64, 58


FONT = "assets/x8y12pxTheStrongGamer.ttf"


class App:
    def __init__(self):
        pyxel.init(144, 144, title="Pyxel Clock", fps=10, display_scale=4)
        self.font = pyxel.Font(FONT, font_size=12)
        self.display_mode = "time"  # time or date
        pyxel.run(self.update, self.draw)

    def update(self):
        quit_by_keyboard = pyxel.btnp(pyxel.KEY_Q)
        quit_by_gamepad = pyxel.btn(pyxel.GAMEPAD1_BUTTON_START) and pyxel.btn(
            pyxel.GAMEPAD1_BUTTON_BACK
        )

        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.display_mode = "date" if self.display_mode == "time" else "time"

        if quit_by_keyboard or quit_by_gamepad:
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        now = datetime.datetime.now()
        draw_face(CX, CY, R)
        draw_hands(CX, CY, now.hour, now.minute, now.second)
        if self.display_mode == "time":
            pyxel.text(28, 124, now.strftime("%p %I:%M:%S"), 7, self.font)
        elif self.display_mode == "date":
            pyxel.text(16, 124, now.strftime("%Y/%m/%d %a"), 7, self.font)


def run():
    App()
