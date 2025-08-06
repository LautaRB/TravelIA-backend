from django.db import models
from viaje.models import Viaje

class Medio(models.Model):
    viaje = models.ForeignKey("viaje.Viaje", on_delete=models.CASCADE, related_name="medios")
    
    TYPE_CHOICES = [
        ("TERRESTRE", "Terrestre"),
        ("MARITIMO", "Marítimo"),
        ("AEREA", "Aérea"),
        ("SIN DEFINIR", "Sin definir"),
        ("PÚBLICO COMBINADO", "Público combinado"),
        ("PRIVADO COMBINADO", "Privado combinado"),
        ("SIN DEFINIR", "Sin definir"),
    ]

    nombre_Medio = models.CharField(max_length=50)
    tipo = models.CharField(choices=TYPE_CHOICES, default="SIN DEFINIR", max_length=20)

    def __str__(self):
        return f"{self.nombre_Medio} - {self.tipo}"
