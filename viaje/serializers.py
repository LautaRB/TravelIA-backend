from rest_framework import serializers
from .models import Viaje
from ruta.serializers import RutaSerializer
from medio.serializers import MedioSerializer
from travelia.utils.messeges import MessagesES

class ViajeSerializer(serializers.ModelSerializer):
    ruta = RutaSerializer(read_only=True)
    medio = MedioSerializer(read_only=True)

    class Meta:
        model = Viaje
        fields = ['id', 'titulo', 'user', 'ruta', 'medio', 'fecha_inicio', 'fecha_fin']

    def validate_fecha_inicio(self, date):
        if date < date.today():
            raise serializers.ValidationError(MessagesES.ERROR_DATE_PAST)
        return date
    
    def validate_fecha_fin(self, date):
        if date < date.today():
            raise serializers.ValidationError(MessagesES.ERROR_DATE_PAST)
        return date
    
    def validate_fechas(self, data):
        if data['fecha_inicio'] > data['fecha_fin']:
            raise serializers.ValidationError(MessagesES.ERROR_DATES)
        return data
