from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from cloudinary.models import CloudinaryField
import cloudinary

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
    
    CURRENCY_CHOICES = [
        ('USD', 'Dólares (USD)'),
        ('ARS', 'Pesos Arg (ARS)'),
        ('EUR', 'Euros (EUR)'),
    ]
    UNIT_CHOICES = [
        ('KM', 'Kilómetros'),
        ('MI', 'Millas'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(choices=ROLE_CHOICES, default="USER", max_length=10)

    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='ARS')
    distance_unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default='KM')
    
    profile_picture = CloudinaryField(
        "profile_picture",
        blank=True,
        null=True
    )

    google_profile_picture = models.URLField(max_length=500, blank=True, null=True)
    
    objects = UserManager()

    def __str__(self):
        return f"{self.username} - {self.role}"

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            try:
                return cloudinary.CloudinaryImage(str(self.profile_picture)).build_url(secure=True)
            except Exception:
                return None
        
        if self.google_profile_picture:
            return self.google_profile_picture
            
        return None
