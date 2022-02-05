from PIL import Image, ImageDraw
from tag_faces import *
from params import *
import face_recognition

# List of bool flags for filters
# isSunglasses, isClown, isLipColor, isEyeLiner, isEyeSparkle

pref = {"isSunglasses": True, 
        "isClown": True,
        "isLipColor": True,
        "isEyeLiner": True,
        "isEyeSparkle": True,
        "isEyebrows": True}

image = face_recognition.load_image_file(f"{PICDIR}{PICTURE}")
face_landmarks_list = face_recognition.face_landmarks(image)

print(face_landmarks_list)

pil_image = Image.fromarray(image)
for face_landmarks in face_landmarks_list:
    draw = ImageDraw.Draw(pil_image, 'RGBA')

    if pref["isEyebrows"]:
        draw.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
        draw.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))

    if pref["isLipColor"]:
        draw.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 88))
        draw.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 88))

    if pref["isEyeSparkle"]:
        draw.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
        draw.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

    if pref["isEyeLiner"]:
        draw.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=1)
        draw.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=1)
    
    if pref["isClown"]:
        img_nose = Image.open('img_components/clown_nose.png')
        draw.line(face_landmarks['nose_tip'], fill=(150, 0, 0, 64), width=8)
        counter, cx, cy = 0, 0, 0
        min_x, min_y, max_x, max_y = 999999999, 999999999, 0, 0
        for coord in face_landmarks['nose_tip']:
            counter += 1
            curr_x, curr_y = coord[0], coord[1]
            if curr_x < min_x:
                min_x = curr_x
            if curr_y < min_y:
                min_y = curr_y
            if curr_x > max_x:
                max_x = curr_x
            if curr_y > max_y:
                max_y = curr_y
        print(min_x, min_y, max_x, max_y)
        nose_coords = (int(cx / counter), int(cy / counter))
        cx = int((min_x + max_x) / 2)
        cy = int((min_y + max_y) / 2)
        r = abs(max_x - min_x)

        draw.ellipse((min_x, cy - .5 * r, max_x, cy + .5 * r), fill=(255, 0, 0), outline=(0, 0, 0, 255), width=0)

    pil_image.show()
    pil_image.save(f"{OUTDIR}beautified_{PICTURE}")