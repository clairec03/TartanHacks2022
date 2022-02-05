from django.db import models
import numpy

# Create your models here.
class CustomEncodingManager(BaseEncodingManager):
    def create_encoding(self, encoding_obj):
        encoding_list = numpy.ndarray.tolist(encoding_obj)
        encoding = self.model(serialized_encoding = encoding_list)
        encoding.save()
        return encoding


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

class Encoding(models.Model):
    serialized_encoding = models.JSONField()
    person = models.ForeignKey(User)