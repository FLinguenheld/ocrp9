from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

import os
from PIL import Image


class User(AbstractUser):
    PHOTO_SIZE = (70, 70)
    EMPTY_FILE_NAME = 'empty_avatar.png'

    photo = models.ImageField(default=f'{settings.MEDIA_ROOT}/{EMPTY_FILE_NAME}',
                              verbose_name='Photo de profil')

    def save(self, *args, **kwargs):

        # Renames and removes the old file
        self.photo.name = f'{self.first_name}_{self.last_name}_Photo.png'
        if os.path.exists(self.photo.path):
            os.remove(self.photo.path)

        # LE PATH est toujours bon :| ?????????????????????????????????????????????


        # Saves (it will write a new photo with the right name, except for empty form)
        super().save(*args, **kwargs)

        # Then resizes and saves
        if os.path.exists(self.photo.path):
            p = Image.open(self.photo)
        else:
            p = Image.open(f'{settings.MEDIA_ROOT}/{self.EMPTY_FILE_NAME}')

        p = p.resize(self.PHOTO_SIZE)
        p.save(self.photo.path, 'png')
