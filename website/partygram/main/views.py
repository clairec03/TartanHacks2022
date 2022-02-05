import encodings
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
import face_recognition
from main.models import Profile, Encoding, Image
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
import numpy as np
import json, logging
from django.conf import settings
import os
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.is_admin = True
            new_profile = Profile(user=user)
            new_profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
    # form_class = UserCreationForm
    # success_url = reverse_lazy('login')
    # template_name = 'registration/signup.html'

@login_required
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        image_upload(uploaded_file)
    return render(request, 'home.html', context)

@login_required
def prof_pic_upload(request):
    user_m = request.user
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        profile = Profile.objects.get(user=user_m)
        profile.pfp = uploaded_file
        profile.save()
        logging.warning(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".." + profile.pfp.url))
        npencoding = get_encoding(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".." + profile.pfp.url))
        json_encoding = json.dumps(npencoding.tolist())
        encoding = Encoding(user = profile, serialized_encoding=json_encoding)
        encoding.save()


    return render(request, 'home.html', context)


def image_upload(image_file):
    picture = face_recognition.load_image_file(image_file)
    face_locations = face_recognition.face_locations(
            picture,
            number_of_times_to_upsample=1
    )

    image = Image(image_file = image_file)
    image.save()

    for face_location in face_locations:
        top, right, bottom, left = face_location
        face = picture[top:bottom, left:right]
        encoding = face_recognition.face_encodings(face)
        if len(encoding) == 0:
            continue
        encoding = encoding[0]

        #  Image.fromarray(face).show()
        profiles = Profile.objects.all()
        
        for profile in profiles:
            user_encodings = Encoding.objects.filter(user=profile)
            if len(user_encodings) == 0:
                continue
            user_encoding = user_encodings[0].get_numpy_array()
            result = face_recognition.compare_faces([encoding], user_encoding)
            if result[0]:
                image.people.add(profile)
                logging.warning(profile.user.username)
                # Image.fromarray(face).show()
                # Image.fromarray(user_face).show()
    
    
    image.save()

def get_encoding(img_url):
    picture = face_recognition.load_image_file(img_url)
    logging.warning("read picture done")
    face_location = face_recognition.face_locations(
            picture,
            number_of_times_to_upsample=1,
            model="cnn"
    )[0]
    top, right, bottom, left = face_location
    face = picture[top:bottom, left:right]
    encoding = face_recognition.face_encodings(face)
    logging.warning(encoding)
    if len(encoding) <= 0:
        return None
    else:
        return encoding[0]
