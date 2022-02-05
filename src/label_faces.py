from PIL import Image, ImageDraw
import face_recognition
import os
from tag_faces import *
from params import *
import sys

with Image.open(f"{PICDIR}{PICTURE}") as im:
    for uname in matches:
        for pic_coords in matches[uname]:
            pic = pic_coords[0]
            if PICTURE == pic:
                coords = pic_coords[1]
                (x0, x1) = (coords[3], coords[1])
                (y0, y1) = (coords[0], coords[2])
            
                draw = ImageDraw.Draw(im, 'RGBA')
                # (x0, y0, x1, y1)
                draw.line([(x0, y0), (x1, y0)], fill=(93, 249, 7, 227)) # Upper horizontal line
                draw.line([(x0, y1), (x1, y1)], fill=(93, 249, 7, 227)) # Lower horizontal line
                draw.line([(x0, y0), (x0, y1)], fill=(93, 249, 7, 227)) # Left vertical line
                draw.line([(x1, y0), (x1, y1)], fill=(93, 249, 7, 227)) # Right vertical line
                im.save(f"{OUTDIR}tagged_{PICTURE}")