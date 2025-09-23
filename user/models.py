from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from cloudinary.models import CloudinaryField

class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un email")
        email = self.normalize_email(email)
        extra_fields.setdefault('role', 'USER')
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'SUPERUSER')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ("SUPERUSER", "SUPERUSER"),
        ("USER", "USER"),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(choices=ROLE_CHOICES, default="USER", max_length=10)

    profile_picture = CloudinaryField(
        "profile_picture",
        default="default_opw0zi",
        blank=True,
        null=True
    )

    objects = UserManager()

    def __str__(self):
        return f"{self.username} - {self.role}"

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            if self.profile_picture.startswith("http"):
                return self.profile_picture 
            return f"/media/{self.profile_picture}"
        return "/media/profile_pictures/default.png"
