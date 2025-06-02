from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    ROLE = [
            ("ADMIN", "ADMIN"),
            ("USER", "USER")
    ]
    role = models.CharField(choices=ROLE, default=ROLE[1])

    def __str__(self): #Para ver el nombre en la BD
        return self.username + ' - ' + self.role