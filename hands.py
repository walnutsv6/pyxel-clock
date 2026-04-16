import pyxel
from utils import angle_to_xy


def draw_hands(cx, cy, h, m, s, show_hour=True):
    sec_fraction  = s / 60
    min_fraction  = (m + s / 60) / 60
    hour_fraction = ((h % 12) + m / 60) / 12

    # 時針
    if show_hour:
        hx, hy = angle_to_xy(cx, cy, 32, hour_fraction)
        htx, hty = angle_to_xy(cx, cy, -8, hour_fraction)
        pyxel.line(htx, hty, hx, hy, 7)
        hx2, hy2 = angle_to_xy(cx + 1, cy, 32, hour_fraction)
        htx2, hty2 = angle_to_xy(cx + 1, cy, -8, hour_fraction)
        pyxel.line(htx2, hty2, hx2, hy2, 7)

    # 分針
    mx, my = angle_to_xy(cx, cy, 48, min_fraction)
    mtx, mty = angle_to_xy(cx, cy, -10, min_fraction)
    pyxel.line(mtx, mty, mx, my, 7)
    mx2, my2 = angle_to_xy(cx + 1, cy, 48, min_fraction)
    mtx2, mty2 = angle_to_xy(cx + 1, cy, -10, min_fraction)
    pyxel.line(mtx2, mty2, mx2, my2, 7)

    # 秒針
    sx, sy = angle_to_xy(cx, cy, 52, sec_fraction)
    stx, sty = angle_to_xy(cx, cy, -14, sec_fraction)
    pyxel.line(stx, sty, sx, sy, 8)
