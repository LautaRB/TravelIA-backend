from rest_framework import serializers
from .models import Medio

class MedioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medio
        fields = ['id', 'nombre', 'tipo']
