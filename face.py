import pyxel
from utils import angle_to_xy


def draw_face(cx, cy, radius):
    # 背景・ベゼル
    pyxel.circ(cx, cy, radius, 1)
    pyxel.circb(cx, cy, radius, 2)
    pyxel.circb(cx, cy, radius - 1, 6)

    # 時間目盛り (12本)
    for i in range(12):
        fraction = i / 12
        x1, y1 = angle_to_xy(cx, cy, radius - 3, fraction)
        x2, y2 = angle_to_xy(cx, cy, radius - 7, fraction)
        pyxel.line(x1, y1, x2, y2, 6)

    # 分目盛り (60本、5の倍数はスキップ)
    for i in range(60):
        if i % 5 == 0:
            continue
        fraction = i / 60
        x1, y1 = angle_to_xy(cx, cy, radius - 2, fraction)
        x2, y2 = angle_to_xy(cx, cy, radius - 4, fraction)
        pyxel.line(x1, y1, x2, y2, 13)

    # 中心ピボット
    pyxel.circ(cx, cy, 2, 11)
