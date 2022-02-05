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

result = dict()

for face_location in face_locations:
    top, right, bottom, left = face_location
    face_image = picture[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.show()
    print(PICTURE)
    for file in os.listdir(rootdir):
        print(file)
        d = os.path.join(rootdir, file)
        known_image = face_recognition.load_image_file(f"{file}/init.jpg")
        unknown_image = face_recognition.load_image_file(f"{PICTURE}")
        known_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        if os.path.isdir(d) and result[0]:
            print(f"Face matched! Image features {face_location} who is {file}")