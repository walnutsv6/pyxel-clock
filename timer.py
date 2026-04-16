import math
import datetime
import pyxel
from face import draw_face
from hands import draw_hands

CX, CY, R = 72, 64, 58


def draw_timer(remaining, set_seconds, running, done, time_display_mode, font):
    # 表示上の残り時間は切り上げて+1秒ズレを解消
    display_total = math.ceil(remaining)
    minutes = display_total // 60
    seconds = display_total % 60

    draw_face(CX, CY, R)
    
    # タイマーモード表示（12時位置の内側）
    pyxel.text(62, 24, "TIMER", 5)
    # 現在時刻（盤面下半分中央）
    now = datetime.datetime.now()
    now_str = (
        now.strftime("%H:%M")
        if time_display_mode == "24h"
        else now.strftime("%p %I:%M")
    )
    now_x = (144 - len(now_str) * 8) // 2
    pyxel.text(now_x, 84, now_str, 5, font)

    draw_hands(CX, CY, 0, minutes, seconds, show_hour=False)

    # デジタル時間表示
    time_str = f"{minutes:02d}:{seconds:02d}"
    time_x = (144 - len(time_str) * 8) // 2

    if done:
        time_color = 8 if (pyxel.frame_count // 5) % 2 == 0 else 0
    elif remaining <= 30:
        time_color = 10  # 残り30秒以下: 黄色
    elif running:
        time_color = 7
    elif remaining < set_seconds:
        time_color = 13  # 一時停止中
    else:
        time_color = 6   # 開始前

    pyxel.text(time_x, 124, time_str, time_color, font)
