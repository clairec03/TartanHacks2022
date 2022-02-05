from PIL import Image
from params import *
import face_recognition
import os


picture = face_recognition.load_image_file(PICTURE)
rootdir = ROOTDIR

face_locations = face_recognition.face_locations(
        picture,
        number_of_times_to_upsample=0,
        model="cnn"
        )

print(len(face_locations))

for file in os.listdir(rootdir):
    d = os.path.join(rootdir, file)
    if os.path.isdir(d):
        print(d)

for face_location in face_locations:
    top, right, bottom, left = face_location
    face_image = picture[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.show()
