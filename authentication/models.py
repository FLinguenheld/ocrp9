from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

import os
from PIL import Image


class User(AbstractUser):
    PHOTO_SIZE = (60, 60)

    photo = models.ImageField(blank=True, verbose_name='Photo de profil')

    def resize_photo(self):
        """ Opens and resizes the photo field. """
        if self.photo and os.path.exists(self.photo.path):
            p = Image.open(self.photo)
            p = p.resize(self.PHOTO_SIZE)
            p.save(self.photo.path, 'png')
