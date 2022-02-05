from PIL import Image, ImageDraw
from params import *
from tagger import *

if __name__ == "__main__":
    picture = PICDIR + PICTURE
    tagger = Tagger(picture)
    users = tagger.getUsers()
    print(users)
    with Image.open(picture) as im:
        for user in users:
            for location in tagger.getLocations(user):
                y0, x1, y1, x0 = location
                draw = ImageDraw.Draw(im, 'RGBA')
                # (x0, y0, x1, y1)
                draw.line([(x0, y0), (x1, y0)], fill=(93, 249, 7, 227)) # Upper horizontal line
                draw.line([(x0, y1), (x1, y1)], fill=(93, 249, 7, 227)) # Lower horizontal line
                draw.line([(x0, y0), (x0, y1)], fill=(93, 249, 7, 227)) # Left vertical line
                draw.line([(x1, y0), (x1, y1)], fill=(93, 249, 7, 227)) # Right vertical line
                display_name = ""
                for string in user.split("_"):
                    first_char = string[0].upper()
                    rem_chars = string[1:]
                    display_name += first_char
                    display_name += rem_chars
                    display_name += " "
                draw.text((x0, y1 + 10), display_name, fill=(93, 249, 7, 227), anchor="mm") # Displays name
        im.save(OUTDIR + PICTURE)
