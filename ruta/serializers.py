from rest_framework import serializers
from .models import Ruta
from travelia.utils.messeges import MessagesES

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = ['id', 'origen', 'destino', 'km', 'tiempo']

    def validate_origen(self, value):
        if value.isdigit():
            raise serializers.ValidationError(MessagesES.ERROR_ORIGIN_TYPE)
        return value
    
    def validate_destino(self, value):
        if value.isdigit():
            raise serializers.ValidationError(MessagesES.ERROR_DESTINATION_TYPE)
        return value
    
    def validate_km(self, value):
        if isinstance(value, str) or value < 0:
            raise serializers.ValidationError(MessagesES.ERROR_KM_TIME_TYPE)
        return value
    
    def validate_tiempo(self, value):
        if isinstance(value, str) or value < 0:
            raise serializers.ValidationError(MessagesES.ERROR_KM_TIME_TYPE)
        return value
