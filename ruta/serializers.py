from rest_framework import serializers
from .models import Ruta

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = ['id', 'origen', 'destino', 'km', 'tiempo']
