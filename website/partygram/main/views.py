from django.shortcuts import render
from .models import User, Encoding, Image
# Create your views here.

def upload(request):
    return render(request, 'home.html')
