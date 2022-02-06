from PIL import Image
from params import *
from tagger import Tagger
from painter import drawLabel, drawEyebrows, drawLips, drawSparkles, drawEyeliners, drawClownNose, drawSunglasses


def main():
    picture = PICDIR + "picture" + input("Please enter picture #: ") + ".jpg"
    tagger = Tagger(picture)
    users = tagger.getUsers()
    with Image.open(picture) as image:
        for user in users:
            for landmark in tagger.getLandmarks(user):
                drawEyebrows(image, landmark)
                drawLips(image, landmark)
                drawSparkles(image, landmark)
                drawEyeliners(image, landmark)
                drawClownNose(image, landmark)
                drawSunglasses(image, landmark)

            for location in tagger.getLocations(user):
                drawLabel(image, location, user)
        image.show()
        #  image.save(OUTDIR + PICTURE)


if __name__ == "__main__":
    main()
