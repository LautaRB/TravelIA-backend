from django.db import models

# Create your models here.
class Alojamiento(models.Model):
    tipo_sugerido = models.CharField(max_length=255)
    plataforma_recomendada = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo_sugerido} ({self.plataforma_recomendada})"