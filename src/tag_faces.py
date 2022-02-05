from PIL import Image
import face_recognition
import os
from params import *


picture = face_recognition.load_image_file(PICDIR + PICTURE)
face_locations = face_recognition.face_locations(
        picture,
        number_of_times_to_upsample=1,
        model="cnn"
        )

for face_location in face_locations:
    top, right, bottom, left = face_location
    face = picture[top:bottom, left:right]
    encoding = face_recognition.face_encodings(face)
    if len(encoding) == 0:
        continue
    encoding = encoding[0]

    #  Image.fromarray(face).show()
    
    for user in os.listdir(USRDIR):
        if user == ".DS_Store":
            continue
        user_face = face_recognition.load_image_file(os.path.join(USRDIR, user) + "/init.jpg")
        user_encoding = face_recognition.face_encodings(user_face)
        if len(user_encoding) == 0:
            continue
        user_encoding = user_encoding[0]
        result = face_recognition.compare_faces([encoding], user_encoding)
        if result[0]:
            print(user)
            Image.fromarray(face).show()
            Image.fromarray(user_face).show()
