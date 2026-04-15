import math


def angle_to_xy(cx, cy, radius, fraction):
    """fraction: 0.0=12時, 0.5=6時 (時計回り)"""
    angle = fraction * 2 * math.pi - math.pi / 2
    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)
    return int(round(x)), int(round(y))
