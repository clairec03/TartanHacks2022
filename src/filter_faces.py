from PIL import ImageDraw
from tagger import *


def drawEyebrows(image, landmark):
    draw = ImageDraw.Draw(image, 'RGBA')
    draw.polygon(landmark['left_eyebrow'], fill=(68, 54, 39, 128))
    draw.polygon(landmark['right_eyebrow'], fill=(68, 54, 39, 128))

def drawLips(image, landmark):
    draw = ImageDraw.Draw(image, 'RGBA')
    draw.polygon(landmark['top_lip'], fill=(150, 0, 0, 88))
    draw.polygon(landmark['bottom_lip'], fill=(150, 0, 0, 88))

def drawSparkles(image, landmark):
    draw = ImageDraw.Draw(image, 'RGBA')
    draw.polygon(landmark['left_eye'], fill=(255, 255, 255, 30))
    draw.polygon(landmark['right_eye'], fill=(255, 255, 255, 30))

def drawEyeliners(image, landmark):
    draw = ImageDraw.Draw(image, 'RGBA')
    draw.line(landmark['left_eye'][0:int(len(landmark['left_eye']) / 1.5)], fill=(0, 0, 0, 110), width=2)
    draw.line(landmark['right_eye'][0:int(len(landmark['right_eye']) / 1.5)], fill=(0, 0, 0, 110), width=2)

def drawClownNose(image, landmark):
    draw = ImageDraw.Draw(image, 'RGBA')
    counter, cx, cy = 0, 0, 0
    min_x, min_y, max_x, max_y = 999999999, 999999999, 0, 0
    for coord in landmark['nose_tip']:
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
    cx = int((min_x + max_x) / 2)
    cy = int((min_y + max_y) / 2)
    d = abs(max_x - min_x) * 1.5
    draw.ellipse((cx - 0.5 * d, cy - 0.5 * d, cx + 0.5 * d, cy + 0.5 * d), fill=(250, 0, 0), outline=(80, 0, 0, 255), width=1)

def drawSunglasses(image, landmark):
    draw = ImageDraw.Draw(image, 'RGBA')
    smol_x, lorge_x = (landmark['left_eye'][0][0] + landmark['left_eyebrow'][0][0]) / 2, (landmark['left_eye'][int(len(landmark['left_eye'])/1.5)][0] + landmark['left_eyebrow'][int(len(landmark['left_eyebrow'])/1.5)][0]) / 2
    smol_y, lorge_y = landmark['left_eye'][0][1], landmark['left_eye'][int(len(landmark['left_eye'])/1.5)][1]
    avg_x = (smol_x + lorge_x) / 2
    avg_y = (smol_y + lorge_y) / 2
    r = (lorge_x - smol_x) / 1.1
    draw.ellipse((avg_x - r, avg_y - r, avg_x + r, avg_y + r), fill=(60, 60, 60, 128), outline=(70, 70, 70, 255), width=1)
    smol_bridge = (lorge_x, avg_y)

    smol_x, lorge_x = (landmark['right_eye'][0][0] + landmark['right_eyebrow'][0][0]) / 2, (landmark['right_eye'][int(len(landmark['right_eye'])/1.5)][0] + landmark['right_eyebrow'][int(len(landmark['right_eyebrow'])/1.5)][0]) / 2
    smol_y, lorge_y = landmark['right_eye'][0][1], landmark['right_eye'][int(len(landmark['right_eye'])/1.5)][1]
    avg_x = (smol_x + lorge_x) / 2
    avg_y = (smol_y + lorge_y) / 2
    r = (lorge_x - smol_x) / 1.1
    draw.ellipse((avg_x - r, avg_y - r, avg_x + r, avg_y + r), fill=(60, 60, 60, 128), outline=(70, 70, 70, 255), width=1)
    lorge_bridge = (smol_x, avg_y)
    draw.line([smol_bridge, lorge_bridge], fill=(65, 65, 65, 128), width=3)
