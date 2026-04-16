import math
import pyxel
import datetime
from face import draw_face
from hands import draw_hands
from timer import draw_timer

CX, CY, R = 72, 64, 58


FONT = "assets/x8y12pxTheStrongGamer.ttf"


def format_current_time(now, display_mode, include_seconds=False):
    if display_mode == "24h":
        time_format = "%H:%M:%S" if include_seconds else "%H:%M"
    else:
        time_format = "%p %I:%M:%S" if include_seconds else "%p %I:%M"
    return now.strftime(time_format)


def centered_text_x(text, char_width=8, screen_width=144):
    return (screen_width - len(text) * char_width) // 2


class App:
    def __init__(self):
        pyxel.init(144, 144, title="Pyxel Clock", fps=10, display_scale=4)
        pyxel.load("clock.pyxres")
        self.font = pyxel.Font(FONT, font_size=12)
        self.display_page = "clock"
        self.display_mode = "time"  # time or date
        self.time_display_mode = "12h"  # 12h or 24h
        self.timer_set_seconds = 300
        self.timer_remaining = 300.0
        self.timer_running = False
        self.timer_done = False
        pyxel.run(self.update, self.draw)

    def update(self):
        quit_by_keyboard = pyxel.btnp(pyxel.KEY_Q)
        quit_by_gamepad = pyxel.btn(pyxel.GAMEPAD1_BUTTON_START) and pyxel.btn(
            pyxel.GAMEPAD1_BUTTON_BACK
        )
        if quit_by_keyboard or quit_by_gamepad:
            pyxel.quit()

        if self.display_page == "clock":
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.display_mode = "date" if self.display_mode == "time" else "time"
            if pyxel.btnp(pyxel.KEY_R) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.time_display_mode = "24h" if self.time_display_mode == "12h" else "12h"
            if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                self.display_page = "timer"

        elif self.display_page == "timer":
            # 戻る
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                if self.timer_done:
                    pyxel.stop()
                self.display_page = "clock"

            # スタート/一時停止
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                if self.timer_done:
                    pass
                else:
                    self.timer_running = not self.timer_running

            # リセット
            if pyxel.btnp(pyxel.KEY_R) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                pyxel.stop()
                self.timer_remaining = float(self.timer_set_seconds)
                self.timer_running = False
                self.timer_done = False

            # 時間調整（未実行時のみ、長押しで連続変更）
            if not self.timer_running and not self.timer_done:
                if pyxel.btnp(pyxel.KEY_UP, 10, 3) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP, 10, 3):
                    self.timer_set_seconds = min(self.timer_set_seconds + 60, 3600)
                    self.timer_remaining = float(self.timer_set_seconds)
                if pyxel.btnp(pyxel.KEY_DOWN, 10, 3) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN, 10, 3):
                    self.timer_set_seconds = max(self.timer_set_seconds - 60, 60)
                    self.timer_remaining = float(self.timer_set_seconds)

        # カウントダウン更新（画面に関わらず常に動作）
        if self.timer_running:
            self.timer_remaining -= 0.1
            if self.timer_remaining <= 0:
                self.timer_remaining = 0
                self.timer_running = False
                self.timer_done = True
                pyxel.playm(0, loop=True)

    def draw(self):
        pyxel.cls(0)
        if self.display_page == "clock":
            now = datetime.datetime.now()
            draw_face(CX, CY, R)
            draw_hands(CX, CY, now.hour, now.minute, now.second)
            if self.display_mode == "time":
                time_text = format_current_time(
                    now, self.time_display_mode, include_seconds=True
                )
                pyxel.text(
                    centered_text_x(time_text),
                    124,
                    time_text,
                    7,
                    self.font,
                )
            elif self.display_mode == "date":
                pyxel.text(16, 124, now.strftime("%Y/%m/%d %a"), 7, self.font)
            timer_active = (
                self.timer_running
                or self.timer_done
                or self.timer_remaining < self.timer_set_seconds
            )
            if timer_active:
                blink_on = (pyxel.frame_count // 5) % 2 == 0
                if not self.timer_running and not self.timer_done:
                    pyxel.blt(108, 2, 0, 32, 0, 8, 8, 0)  # 一時停止中は常時表示
                elif blink_on:
                    pyxel.blt(108, 2, 0, 32, 0, 8, 8, 0)  # 動作中/完了は点滅
                display_total = math.ceil(self.timer_remaining)
                m = display_total // 60
                s = display_total % 60
                time_str = f"{m:02d}:{s:02d}"
                if self.timer_done:
                    text_color = 8 if blink_on else 0
                elif self.timer_remaining <= 30:
                    text_color = 10  # 残り30秒以下: 黄色
                elif self.timer_running:
                    text_color = 7   # 動作中: 白
                else:
                    text_color = 5   # 一時停止中: グレー
                pyxel.text(120, 4, time_str, text_color)
        elif self.display_page == "timer":
            pyxel.blt(108, 2, 0, 32, 0, 8, 8, 0)  # タイマーモードアイコン
            draw_timer(
                self.timer_remaining,
                self.timer_set_seconds,
                self.timer_running,
                self.timer_done,
                self.time_display_mode,
                self.font,
            )


def run():
    App()
