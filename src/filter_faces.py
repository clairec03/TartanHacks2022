from PIL import Image, ImageDraw
from tag_faces import *
from params import *
import face_recognition

PICTURE = "picture4.jpg"

# List of bool flags for filters
# isSunglasses, isClown, isLipColor, isEyeLiner, isEyeSparkle

pref = {"isSunglasses": True, 
        "isClown": True,
        "isLipColor": True,
        "isEyeLiner": True,
        "isEyeSparkle": True,
        "isDarkerEyebrows": True}

image = face_recognition.load_image_file(f"{PICDIR}{PICTURE}")
face_landmarks_list = face_recognition.face_landmarks(image)

pil_image = Image.fromarray(image)
for face_landmarks in face_landmarks_list:
    draw = ImageDraw.Draw(pil_image, 'RGBA')

    if pref["isSunglasses"]:
        draw.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
        draw.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
        draw.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)
        draw.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)

    if pref["isLipColor"]:
        draw.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
        draw.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
        draw.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=8)
        draw.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=8)

    if pref["isEyeSparkle"]:
        draw.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
        draw.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

    if pref["isEyeLiner"]:
        draw.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=6)
        draw.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)

    pil_image.show()
    pil_image.save(f"{OUTDIR}beautified_{PICTURE}")