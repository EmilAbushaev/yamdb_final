from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CHOICE_STATUS = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    bio = models.TextField('Биография',)
    role = models.CharField(
        default='user',
        choices=CHOICE_STATUS,
        max_length=20)
    email = models.EmailField(
        max_length=254,
        unique=True,
    )

    def is_user(self):
        if self.role == 'user':
            return True
        return False

    def is_moderator(self):
        if self.role == 'moderator':
            return True
        return False

    def is_admin(self):
        if self.role == 'admin':
            return True
        return False

    class Meta:
        ordering = ['id']
