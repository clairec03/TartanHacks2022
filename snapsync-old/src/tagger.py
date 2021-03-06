import os
import numpy as np
from face_recognition import load_image_file, face_locations, face_landmarks, face_encodings, compare_faces, face_distance

from params import *


class Tagger:
    def __init__(self, picture_path):
        self._picture = load_image_file(picture_path)
        self._data = {USRANON : []}
        self._tag()

    def _tag(self):
        locations = face_locations(self._picture, number_of_times_to_upsample=1, model="cnn")
        landmarks = face_landmarks(self._picture, locations, model="large")
        encodings = face_encodings(self._picture, locations, num_jitters=10, model="large")
        assert len(locations) == len(landmarks) == len(encodings)

        users = []
        user_encodings = []
        for folder in os.scandir(USRDIR):
            if folder.is_dir():
                user = folder.name
                users.append(user)
                user_encoding = face_encodings(load_image_file(USRDIR + user + "/init.jpg"))
                user_encodings.append(user_encoding[0])
                self._data[user] = []

        for location, landmark, encoding in zip(locations, landmarks, encodings):
            matches = compare_faces(user_encodings, encoding)
            distances = face_distance(user_encodings, encoding)
            user_index = np.argmin(distances)
            user = users[user_index] if matches[user_index] else USRANON
            self._data[user].append((location, landmark))

    def getUsers(self):
        return self._data.keys()

    def getLocations(self, user):
        return [location for location, _ in self._data[user]]

    def getLandmarks(self, user):
        return [landmark for _, landmark in self._data[user]]
