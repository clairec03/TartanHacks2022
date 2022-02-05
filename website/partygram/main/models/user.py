from django.db import models
from django.contrib.auth.models import AbstractUser

import numpy
from website.partygram.partygram.settings import AUTH_USER_MODEL

# Create your models here.
class CustomEncodingManager(models.Manager):
    def create_encoding(self, encoding_obj, user):
        encoding_list = numpy.ndarray.tolist(encoding_obj)
        encoding = self.model(serialized_encoding = encoding_list, person = user)
        encoding.save()
        return encoding

    # def get_encoding_nparray(self):


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

class Encoding(models.Model):
    serialized_encoding = models.JSONField()
    person = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    objects = CustomEncodingManager()
    def get_numpy_array(self):
        return numpy.array(self.serialized_encoding)
