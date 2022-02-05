from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# from website.partygram.main.views import upload

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    pfp = models.ImageField(upload_to = "uploads/pictures", default=None)


class Encoding(models.Model):
    serialized_encoding = models.JSONField()
    person = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Image(models.Model):
    img = models.ImageField(upload_to = 'uploads/pictures')
    people = models.ManyToManyField(Profile)
