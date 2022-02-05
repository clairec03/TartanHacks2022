from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)

class Encoding(models.Model):
    serialized_encoding = models.JSONField()
    person = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Image(models.Model):
    img = models.ImageField(upload_to = 'uploads/pictures')
    people = models.ManyToManyField(Profile)
