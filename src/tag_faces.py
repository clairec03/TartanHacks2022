from PIL import Image, ImageDraw
import face_recognition
import os
from params import *
import sys

matches = dict()

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
            if user not in matches:
                matches[user] = {(PICTURE, face_location)}
            else:
                matches[user].add((PICTURE, face_location))

for pic in os.listdir(PICDIR):
    print(f"{pic}")
    # with Image.open(f"{PICDIR}pic") as im:
    # for uname in matches:
    #     for pic_coords in matches[uname]:
    #         pic = pic_coords[0]
    #         coords = pic_coords[1]
    #         (x0, x1) = (coords[3], coords[1])
    #         (y0, y1) = (coords[0], coords[2])
            
    #             draw = ImageDraw.Draw(im)
    #             # (x0, y0, x1, y1)
    #             draw.line(x0, y0, x1, y0, fill=128) # Upper horizontal line
    #             draw.line(x0, y1, x1, y1, fill=128) # Lower horizontal line
    #             draw.line(x0, y0, x0, y1, fill=128) # Left vertical line
    #             draw.line(x1, y0, x1, y1, fill=128) # Right vertical line
    #             im.save(f"{user}")



print(matches)