from PIL import Image, ImageDraw
from tagger import *
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
        draw.line(face_landmarks['left_eye'][0:int(len(face_landmarks['left_eye'])/1.5)], fill=(0, 0, 0, 110), width=2)
        draw.line(face_landmarks['right_eye'][0:int(len(face_landmarks['right_eye'])/1.5)], fill=(0, 0, 0, 110), width=2)
    
    if pref["isClown"]:
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
        d = abs(max_x - min_x) * 1.5
        draw.ellipse((cx - .5 * d, cy - .5 * d, cx + .5 * d, cy + .5 * d), fill=(250, 0, 0), outline=(80, 0, 0, 255), width=1)

    if pref["isSunglasses"]:
        smol_x, lorge_x = (face_landmarks['left_eye'][0][0] + face_landmarks['left_eyebrow'][0][0]) / 2, (face_landmarks['left_eye'][int(len(face_landmarks['left_eye'])/1.5)][0] + face_landmarks['left_eyebrow'][int(len(face_landmarks['left_eyebrow'])/1.5)][0]) / 2
        smol_y, lorge_y = face_landmarks['left_eye'][0][1], face_landmarks['left_eye'][int(len(face_landmarks['left_eye'])/1.5)][1]
        avg_x = (smol_x + lorge_x) / 2
        avg_y = (smol_y + lorge_y) / 2
        r = (lorge_x - smol_x) / 1.1
        draw.ellipse((avg_x - r, avg_y - r, avg_x + r, avg_y + r), fill=(60, 60, 60, 128), outline=(70, 70, 70, 255), width=1)
        smol_bridge = (lorge_x, avg_y)

        smol_x, lorge_x = (face_landmarks['right_eye'][0][0] + face_landmarks['right_eyebrow'][0][0]) / 2, (face_landmarks['right_eye'][int(len(face_landmarks['right_eye'])/1.5)][0] + face_landmarks['right_eyebrow'][int(len(face_landmarks['right_eyebrow'])/1.5)][0]) / 2
        smol_y, lorge_y = face_landmarks['right_eye'][0][1], face_landmarks['right_eye'][int(len(face_landmarks['right_eye'])/1.5)][1]
        avg_x = (smol_x + lorge_x) / 2
        avg_y = (smol_y + lorge_y) / 2
        r = (lorge_x - smol_x) / 1.1
        draw.ellipse((avg_x - r, avg_y - r, avg_x + r, avg_y + r), fill=(60, 60, 60, 128), outline=(70, 70, 70, 255), width=1)
        lorge_bridge = (smol_x, avg_y)
        draw.line([smol_bridge, lorge_bridge], fill=(65, 65, 65, 128), width=3)

    pil_image.save(f"{OUTDIR}beautified_{PICTURE}")

res = Image.open(f"{OUTDIR}beautified_{PICTURE}")
res.show()
