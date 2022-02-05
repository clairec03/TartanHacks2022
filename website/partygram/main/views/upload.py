from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
import face_recognition
from main.models import User, Encoding, Image


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(filename)
    return render(request, 'upload.html', context)

def image_processing(image_url):
    picture = face_recognition.load_image_file(image_url)
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

        #  Image.fromarray(face).show()
        users = User.objects.all()
        
        for user in users:
            user_encodings = Encoding.objects.filter(reporter__first_name='John')
            if len(user_encoding) == 0:
                continue
            user_encoding = user_encoding[0]
            result = face_recognition.compare_faces([encoding], user_encoding)
            if result[0]:
                print(user)
                Image.fromarray(face).show()
                Image.fromarray(user_face).show()
    

