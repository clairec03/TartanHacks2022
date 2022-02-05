from PIL import Image, ImageDraw
from params import *
from tagger import *


def toDisplayName(user):
    assert '_' in user
    return ' '.join(name.capitalize() for name in user.split('_'))


if __name__ == "__main__":
    picture = PICDIR + PICTURE
    tagger = Tagger(picture)
    users = tagger.getUsers()
    with Image.open(picture) as image:
        for user in users:
            for location in tagger.getLocations(user):
                top, right, bottom, left = location
                mid = left + (right - left) / 2
                draw = ImageDraw.Draw(image, 'RGBA')
                draw.polygon([(left, top), (left, bottom), (right, bottom), (right, top)],
                        width=LINEWIDTH,
                        outline=OUTLINECLR
                        )
                draw.text((mid, bottom), toDisplayName(user),
                        anchor="ma",
                        font=TEXTFONT,
                        fill=TEXTCLR
                        )
        image.save(OUTDIR + PICTURE)
