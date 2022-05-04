from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from ticket.models import Ticket

class Review(models.Model):

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.fields.PositiveSmallIntegerField(max_length=1024, validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.fields.CharField(max_length=128)
    body = models.fields.TextField()
    time_created = models.fields.DateTimeField(auto_now_add=True)
