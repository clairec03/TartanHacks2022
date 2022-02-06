from multiprocessing import dummy
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from main.models import Profile, Identification, Moment, Face
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
import numpy as np
import json, logging
from django.conf import settings
import os
from face_recognition import load_image_file, face_locations, face_landmarks, face_encodings, compare_faces, face_distance


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
    user = authenticate(username=username, password=password)
    profile = Profile(user=user)
    profile.save()
    login(request, user)
    return redirect('home') 

@login_required
def upload_avatar(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    profile.avatar = request.FILES['document']
    profile.save()
    return render(request, "profile.html", {"profile": profile})

@login_required
def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(request, 'profile.html', {"profile": profile})

@login_required
def upload_identification(request):
    if request.method != "POST":
        return render(request, 'home.html', {})
    
    user = request.user
    profile = Profile.objects.get(user=user)
    temp_path = request.FILES["documents"]
    temp = load_image_file(temp_path)
    encoding = face_encodings(temp, num_jitters=10, model="large")
    identification = Identification(profile=profile, encoding=nparrayToJSON(encoding))
    identification.save()

    return redirect("home")

    # logging.warning(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".." + profile.pfp.url))
    # npencoding = get_encoding(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".." + profile.pfp.url))
    
@login_required
def upload_moment(request):
    if request.method != "POST":
        return render(request, 'upload_moment.html')

    moment = Moment(picture=request.FILES["document"])
    moment.save()

    picture_path = request.FILES['document']
    picture = load_image_file(picture_path)

    logging.warning("asdfdfjklasdj")
    locations = face_locations(picture, number_of_times_to_upsample=1, model="cnn")
    logging.warning("asklasdj")
    landmarks = face_landmarks(picture, locations, model="large")
    logging.warning("jkasdfjklasdj")
    encodings = face_encodings(picture, locations, num_jitters=5, model="large")
    logging.warning("kasdfjklasdj")
    assert len(locations) == len(landmarks) == len(encodings)

    profiles = []
    encodings = []
    for identification in Identification.objects.all():
        profiles.append(identification.profile)
        encodings.append(identification.getEncoding())
    logging.warning("kdj")
    
    for location, landmark, encoding in zip(locations, landmarks, encodings):
        logging.warning("count")
        matches = compare_faces(encodings, encoding)
        distances = face_distance(encodings, encoding)
        index = np.argmin(distances)

        if not matches[index]:
            dummy = User.objects.get(username = "dummy")
            profile[index] = Profile.objects.get(user = dummy)
        else:
            face = Face(
                profile=profiles[index],
                moment=moment,
                location=nparrayToJSON(location),
                landmark=nparrayToJSON(landmark))
            face.save()

    return render(request, 'home.html', {})

@login_required
def image_gallery_view(request):
    user_m = request.user
    user_prof = Profile.objects.get(user=user_m)
    img1 = []
    img2 = []
    img3 = []
    all_faces = user_prof.face_set.all()
    all_img = []
    for face in all_faces:
        all_img.append(face.moment)
    print(len(all_faces))
    # split moment into 3 lists
    index = 0
    for mom in all_img:
        if index % 3 == 0:
            img1.append(mom)
        elif index % 3 == 1:
            img2.append(mom)
        else:
            img3.append(mom)
        index += 1
    return render(request, 'home.html', {'img1':img1, 'img2':img2, 'img3':img3})

def welcome(request):
    if(request.user.is_authenticated):
        return render(request, 'home.html')
    else:
        return render(request, 'welcome.html')

def nparrayToJSON(nparray):
    return json.dumps(nparray.tolist())