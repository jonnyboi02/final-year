from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    private_key = models.CharField(max_length=250)

    def get_key(self):
        return self.private_key
        
        