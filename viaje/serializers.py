from rest_framework import serializers
from .models import Viaje
from ruta.serializers import RutaSerializer
from medio.serializers import MedioSerializer

class ViajeSerializer(serializers.ModelSerializer):
    ruta = RutaSerializer(read_only=True)
    medio = MedioSerializer(read_only=True)

    class Meta:
        model = Viaje
        fields = ['id', 'ruta', 'medio', 'fecha_inicio', 'fecha_fin']

