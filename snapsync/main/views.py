from PIL import Image, ImageDraw
from multiprocessing import dummy
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from main.models import Profile, Identification, Moment, Face, Tagged
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
import numpy as np
from django.core.files.base import ContentFile
import json, logging
from django.conf import settings
from io import BytesIO
import os
from face_recognition import load_image_file, face_locations, face_landmarks, face_encodings, compare_faces, face_distance

def home(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("welcome")

    profile = Profile.objects.get(user=user)
    momentss = [[], [], []]
    faces = profile.face_set.all()
    for index, face in enumerate(faces):
        momentss[index % 3].append(face.moment)
    return render(request, 'home.html', {'momentss': momentss})

def welcome(request):
    return render(request, 'welcome.html')

def signup(request):
    if request.method != "POST":
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
    form = UserCreationForm(request.POST)
    if not form.is_valid():
        return render(request, 'registration/signup.html', {'form': form})
    form.save()

    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password1')
    user = authenticate(
        username=username,
        password=password
        )
    profile = Profile(user=user)
    profile.save()
    login(request, user)
    return redirect('home') 

@login_required
def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(request, 'profile.html', {"profile": profile})

@login_required
def upload_avatar(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    profile.avatar = request.FILES['document']
    profile.save()
    return render(request, "profile.html", {"profile": profile})

@login_required
def upload_identification(request):
    if request.method != "POST":
        return render(request, 'home.html', {})

    user = request.user
    profile = Profile.objects.get(user=user)
    temp_path = request.FILES["document"]
    temp = load_image_file(temp_path)
    encoding = face_encodings(temp, num_jitters=5, model="large")[0]
    identification = Identification(
        profile=profile,
        encoding=json.dumps(encoding.tolist())
        )
    identification.save()
    return redirect("home")

@login_required
def upload_moment(request):
    if request.method != "POST":
        return render(request, 'upload_moment.html')

    picture_path = request.FILES['document']
    picture = load_image_file(picture_path)
    moment = Moment(picture=picture_path)
    moment.save()

    logging.warning("LOCATION")
    locations = face_locations(picture, number_of_times_to_upsample=1, model="hog")
    logging.warning("LANDMARK")
    landmarks = face_landmarks(picture, locations, model="large")
    logging.warning("ENCODING")
    encodings = face_encodings(picture, locations, num_jitters=1, model="large")
    assert len(locations) == len(landmarks) == len(encodings)

    dummy_index = -1
    k_profiles = []
    k_encodings = []
    for index, identification in enumerate(Identification.objects.all()):
        if identification.profile.user.username == "dummy":
            dummy_index = index
        k_profiles.append(identification.profile)
        k_encodings.append(identification.getEncoding())
    assert dummy_index != -1
    logging.warning("K")

    with Image.open(picture_path) as image:
        for location, landmark, encoding in zip(locations, landmarks, encodings):
            logging.warning("ITERA")
            matches = compare_faces(k_encodings, encoding)
            distances = face_distance(k_encodings, encoding)
            index = np.argmin(distances)
            if not matches[index]:
                index = dummy_index
            face = Face(
                profile=k_profiles[index],
                moment=moment,
                location=json.dumps(location),
                landmark=json.dumps(landmark)
            )
            face.save()

            logging.warning("ITERB")
            top, right, bottom, left = location
            mid = left + (right - left) / 2
            draw = ImageDraw.Draw(image, "RGBA")
            draw.polygon(
                [(left, top), (left, bottom), (right, bottom), (right, top)],
                outline=(0, 255, 0, 255)
                )
            draw.text(
                (mid, bottom),
                k_profiles[index].user.username,
                anchor="ma",
                fill=(0, 255, 0, 255)
                )
        logging.warning("saving")
        blob = BytesIO()
        image.save(blob, format="JPEG")
        tagged = Tagged(
            moment=moment,
            picture=ContentFile(blob.getvalue(), "tagged.jpg")
            )
        tagged.save()
        logging.warning("saved")

    return redirect("home")

def view_moment(request, id_int=1):
    moment = Moment.objects.filter(id=id_int)[0]
    tagged = Tagged.objects.filter(moment=moment)
    if tagged:
        tagged = tagged[0]
    else:
        tagged = moment
    return render(request, 'photo.html', {'picture':tagged.picture})