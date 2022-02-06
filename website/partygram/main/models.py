from email.policy import default
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings
import os
import json
import numpy as np


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(default=None)


class Identification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    encoding = models.JSONField()

    def getEncoding(self):
        return np.array(json.loads(self.encoding))


class Moment(models.Model):
    picture = models.ImageField(default=None)


class Face(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE)
    location = models.JSONField()
    landmark = models.JSONField()

    def getLocation(self):
        return json.loads(self.location)
    
    def getLandmark(self):
        return json.loads(self.landmark)