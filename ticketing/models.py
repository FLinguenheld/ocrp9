from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from PIL import Image


class Ticket(models.Model):
    IMAGE_MAX_SIZE = (300, 300)

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_edited = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail(self.IMAGE_MAX_SIZE)
            img.save(self.image.path, quality=100)

    def __str__(self):
        return f'{self.title} - {self.user}'

    def get_type(self):
        """ Used in template to recognise post's type between reviews and tickets """
        return "TICKET"


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_edited = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.headline} - À propos de : {self.ticket}'

    def get_type(self):
        """ Used in template to recognise post's type between reviews and tickets """
        return "REVIEW"

    @property
    def rating_stars(self):
        """ Used in review's template to diplay stars, it converts rating int in a string list like : 'YYYNN' """
        rating = ['Y' for _ in range(self.rating)]
        rating += ['N' for _ in range(self.rating, 5)]
        return rating
