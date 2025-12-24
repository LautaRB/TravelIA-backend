from rest_framework import serializers
from .models import Ruta
from travelia.utils.messeges import MessagesES

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = ['id', 'nombre_Ruta', 'origen', 'destino', 'distancia', 'tiempo']

    def validate_nombre_Ruta(self, value):
        if value.isdigit():
            raise serializers.ValidationError(MessagesES.ERROR_ROUTE_NAME_TYPE)
        return value
    
    def validate_origen(self, value):
        if value.isdigit():
            raise serializers.ValidationError(MessagesES.ERROR_ORIGIN_TYPE)
        return value
    
    def validate_destino(self, value):
        if value.isdigit():
            raise serializers.ValidationError(MessagesES.ERROR_DESTINATION_TYPE)
        return value
    
    def validate_distancia(self, value):
        if value < 0:
            raise serializers.ValidationError(MessagesES.ERROR_KM_TIME_TYPE)
        return value
    
    def validate_tiempo(self, value):
        if value < 0:
            raise serializers.ValidationError(MessagesES.ERROR_KM_TIME_TYPE)
        return value