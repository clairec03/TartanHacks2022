from django.db import models

# Create your models here.

class Image(models.Model):
    img = models.ImageField(upload_to = 'uploads/pictures')
    people = models.ManyToManyField(User)
