from django.db import models
from authentication.models import User


class UserFollows(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        # unique_together = ('user', 'followed_user')  # Will be deprecated
        constraints = [models.UniqueConstraint(fields=['user', 'followed_user'], name='unique_couple')]
        verbose_name = 'User follow'
        verbose_name_plural = 'User follows'

    def __str__(self):
        return f'{self.user} suit {self.followed_user}'
