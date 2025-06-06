from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ("ADMIN", "ADMIN"),
        ("USER", "USER"),
    ]
    role = models.CharField(choices=ROLE_CHOICES, default="USER", max_length=10)

    def __str__(self): # Para ver el nombre y el rol del usuario en la BD
        return f"{self.username} - {self.role}"