from PIL import Image
from params import *
from tagger import Tagger
from labeler import drawLabel


def main():
    picture = PICDIR + "picture" + input("Please enter picture #: ") + ".jpg"
    tagger = Tagger(picture)
    users = tagger.getUsers()
    with Image.open(picture) as image:
        for user in users:
            for location in tagger.getLocations(user):
                drawLabel(image, user, location)
        image.save(OUTDIR + PICTURE)
