from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=True)
    is_support_rep = models.BooleanField(default=False)

    def __str__(self):
        return self.username
