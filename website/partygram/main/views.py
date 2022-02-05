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

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
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
    return render(request, 'upload.html', context)

@login_required
def prof_pic_upload(request):
    user_m = request.user
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        user_m.profile.pfp = uploaded_file

    return render(request, 'home.html', context)
    encoding = get_encoding(image_url)
    encoding_obj = Encoding.objects.create_encoding(encoding, user)

def image_upload(image_file):
    picture = face_recognition.load_image_file(image_file)
    face_locations = face_recognition.face_locations(
            picture,
            number_of_times_to_upsample=1,
            model="cnn"
    )

    res = []

    for face_location in face_locations:
        top, right, bottom, left = face_location
        face = picture[top:bottom, left:right]
        encoding = face_recognition.face_encodings(face)
        if len(encoding) == 0:
            continue
        encoding = encoding[0]

        #  Image.fromarray(face).show()
        users = User.objects.all()
        
        for user in users:
            user_encodings = Encoding.objects.filter(User__id=user.id)
            if len(user_encodings) == 0:
                continue
            user_encoding = user_encodings[0].get_numpy_array
            result = face_recognition.compare_faces([encoding], user_encoding)
            if result[0]:
                res.append(user)
                print(user.name)
                # Image.fromarray(face).show()
                # Image.fromarray(user_face).show()

def get_encoding(image_url):
    picture = face_recognition.load_image_file(image_url)
    face_location = face_recognition.face_locations(
            picture,
            number_of_times_to_upsample=1,
            model="cnn"
    )[0]
    top, right, bottom, left = face_location
    face = picture[top:bottom, left:right]
    encoding = face_recognition.face_encodings(face)
    if len(encoding) <= 0:
        return None
    else:
        return encoding[0]
