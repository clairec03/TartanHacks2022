from email.policy import default
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings
import os

# from website.partygram.main.views import upload

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pfp = models.ImageField(upload_to = "uploads/pictures/", default=None)


class Encoding(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    serialized_encoding = models.JSONField()

class Image(models.Model):
    img = models.ImageField(upload_to = 'uploads/pictures')
    people = models.ManyToManyField(Profile)
