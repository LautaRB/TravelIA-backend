from rest_framework import serializers
from .models import Viaje
from ruta.models import Ruta
from medio.models import Medio
from travelia.utils.messeges import MessagesES


class ViajeSerializer(serializers.ModelSerializer):
    ruta = serializers.PrimaryKeyRelatedField(
        queryset=Ruta.objects.all(),
        required=False,
        allow_null=True
    )
    medio = serializers.PrimaryKeyRelatedField(
        queryset=Medio.objects.all(),
        required=False,
        allow_null=True
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Viaje
        fields = ['id', 'titulo', 'user', 'ruta', 'medio', 'fecha_inicio', 'fecha_fin']
        read_only_fields = ['user']

    def validate_fecha_inicio(self, date):
        if date < date.today():
            raise serializers.ValidationError(MessagesES.ERROR_DATE_START_PAST)
        return date

    def validate_fecha_fin(self, date):
        if date < date.today():
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