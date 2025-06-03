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
    role = models.CharField(choices=ROLE, default="USER", max_length=10)

    def __str__(self): #Para ver el nombre en la BD
        return self.username + ' - ' + self.role
    
    def set_password(self, raw_password):
        self.password = raw_password
        self.save()