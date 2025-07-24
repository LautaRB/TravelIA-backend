from rest_framework import serializers

class PlanViajeSerializer(serializers.Serializer):
    origen = serializers.CharField()
    destino = serializers.CharField()
    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()
