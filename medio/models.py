from django.db import models

class Medio(models.Model):
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
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.nombre_Medio} - {self.tipo}"
