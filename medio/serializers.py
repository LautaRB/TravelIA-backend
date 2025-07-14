from rest_framework import serializers
from travelia.utils.messeges import MessagesES
from .models import Medio

class MedioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medio
        fields = ['id', 'nombre', 'tipo']
    
    def validate_nombre(self, value):
        if value.isdigit():
            raise serializers.ValidationError(MessagesES.ERROR_MEDIA_NAME_TYPE)
        return value
    
    def validate_tipo(self, value):
        if value.isdigit():
            raise serializers.ValidationError(MessagesES.ERROR_MEDIA_TYPE)
        return value
