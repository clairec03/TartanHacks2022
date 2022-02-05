from PIL import ImageDraw
from params import *


def drawLabel(image, user, location):
    assert "_" in user
    top, right, bottom, left = location
    mid = left + (right - left) / 2
    draw = ImageDraw.Draw(image, 'RGBA')
    draw.polygon([(left, top), (left, bottom), (right, bottom), (right, top)],
            width=LINEWIDTH, outline=OUTLINECLR)
    draw.text((mid, bottom), ' '.join(name.capitalize() for name in user.split('_')),
            anchor="ma", font=TEXTFONT, fill=TEXTCLR)
