from django.db import models

class Medio(models.Model):
    TYPE_CHOICES = [
        ("TERRESTRE", "Terrestre"),
        ("MARITIMO", "Maritimo"),
        ("AEREA", "Aerea"),
        ("SIN DEFINIR", "Sin definir"),
        ("PÚBLICO COMBINADO", "Público combinado"),
        ("PRIVADO COMBINADO", "Privado combinado"),
    ]
    nombre_Medio = models.CharField(max_length=50)
    tipo = models.CharField(choices=TYPE_CHOICES, default="Sin definir", max_length=20)

    def __str__(self):
        return f"{self.nombre_Medio} - " + self.tipo