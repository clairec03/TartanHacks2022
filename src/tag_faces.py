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
# (image file name, face_location)

for face_location in face_locations:
    top, right, bottom, left = face_location
    unknown_image = picture[top:bottom, left:right]
    pil_image = Image.fromarray(unknown_image)
    pil_image.show()
    for file in os.listdir(rootdir):
        if not file == ".DS_Store":
            d = os.path.join(rootdir, file)
            known_image = face_recognition.load_image_file(f"{ROOTDIR}{file}/init.jpg")
            known_encoding = face_recognition.face_encodings(known_image)[0]
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            results = face_recognition.compare_faces(known_encoding, unknown_encoding)
            if os.path.isdir(d) and results[0]:
                print(f"Face matched! Image features {face_location} who is {file}")
                # if (PICTURE, face_location) not in result:
                result[(PICTURE, face_location)] = file