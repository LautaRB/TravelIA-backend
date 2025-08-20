from rest_framework import serializers
import datetime
from .models import Viaje
from travelia.utils.messeges import MessagesES


class ViajeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Viaje
        fields = ['id', 'titulo', 'user', 'origen', 'destino', 'fecha_inicio', 'fecha_fin', 'ruta', 'medio']
        read_only_fields = ['user']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = str(instance.user)
        return rep
    
    def validate_fecha_inicio(self, date):
        if date < datetime.date.today():
            raise serializers.ValidationError(MessagesES.ERROR_DATE_START_PAST)
        return date

    def validate_fecha_fin(self, date):
        if date < datetime.date.today():
            raise serializers.ValidationError(MessagesES.ERROR_DATE_END_PAST)
        return date

    def validate(self, data):
        if data['fecha_inicio'] > data['fecha_fin']:
            raise serializers.ValidationError({"fechas": MessagesES.ERROR_DATES})
        return data

    def validate_titulo(self, value):
        if value.isdigit():
            raise serializers.ValidationError(MessagesES.ERROR_TITLE_TYPE)
        return value
    
    def validate_origen(self, value):
        if value.isdigit():
            raise serializers.ValidationError(MessagesES.ERROR_ORIGIN_TYPE)
        return value
    
    def validate_destino(self, value):
        if value.isdigit():
            raise serializers.ValidationError(MessagesES.ERROR_DESTINATION_TYPE)
        return value