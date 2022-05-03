from django.db import models

class Ticket(models.Model):

    title = models.fields.CharField(max_length=128)
    description = models.fields.CharField(max_length=2048)
    # user = model.fields.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # image = models.fields.ImageField(null=True, blank=True)
    time_created = models.fields.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
