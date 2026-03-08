import re
from datetime import date, datetime
from rest_framework import serializers
from .models import Viaje
from ruta.models import Ruta
from medio.models import Medio
from alojamiento.models import Alojamiento
from travelia.utils.messeges import MessagesES
from rest_framework.exceptions import ValidationError

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = ['nombre_Ruta', 'distancia', 'tiempo']

class MedioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medio
        fields = ['nombre_Medio', 'tipo', 'plataforma_recomendada']

class AlojamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alojamiento
        fields = ['id', 'tipo_sugerido', 'plataforma_recomendada']

class PlanificarViajeSerializer(serializers.Serializer):
    origen = serializers.CharField(required=True)
    destino = serializers.CharField(required=True)
    rango_fechas = serializers.CharField(required=True)
    cantidad_personas = serializers.IntegerField(min_value=1, required=True)
    medio_transporte = serializers.CharField(required=True)

    def validate_origen(self, value):
        if value.strip().isdigit(): 
            raise ValidationError(MessagesES.ERROR_ORIGIN_TYPE)
        return value

    def validate_destino(self, value):
        if value.strip().isdigit():
            raise ValidationError(MessagesES.ERROR_DESTINATION_TYPE)
        return value
    
    def validate_rango_fechas(self, value):
        if value.strip().isdigit():
            raise ValidationError("El rango de fechas tiene que tener el formato: AAAA-MM-DD.")
        
        patron_fechas = re.findall(r'\d{4}-\d{2}-\d{2}', value)
        
        if len(patron_fechas) == 2:
            try:
                fecha_inicio = datetime.strptime(patron_fechas[0], '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(patron_fechas[1], '%Y-%m-%d').date()
                
                if fecha_inicio > fecha_fin:
                    raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")
                
                if fecha_inicio < date.today():
                    raise ValidationError("Las fechas del viaje no pueden estar en el pasado.")
                    
            except ValueError:
                pass

        return value
    
    def validate_medio_transporte(self, value):
        if value.strip().isdigit():
            raise ValidationError("El medio de transporte no puede ser numérico.")
            
        medios_permitidos = ["TERRESTRE", "MARITIMO", "AEREA", "SIN DEFINIR", "PÚBLICO COMBINADO", "PRIVADO COMBINADO"]
        
        valor_limpio = value.strip().upper()
        
        if valor_limpio not in medios_permitidos:
            raise ValidationError(f"Medio de transporte no válido. Opciones permitidas: {', '.join(medios_permitidos)}.")
        return valor_limpio
    
    def validate_cantidad_personas(self, value):
        if value < 1:
            raise ValidationError("Debe viajar al menos 1 persona.")
        if value > 50:
            raise ValidationError("El límite máximo por consulta es de 50 personas.")
        return value

class ViajeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ruta = serializers.PrimaryKeyRelatedField(queryset=Ruta.objects.all(), required=False, allow_null=True)
    medio = serializers.PrimaryKeyRelatedField(queryset=Medio.objects.all(), required=False, allow_null=True)
    alojamiento = serializers.PrimaryKeyRelatedField(queryset=Alojamiento.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = Viaje
        fields = ['id', 'titulo', 'user', 'origen', 'destino', 'rango_fechas', 'cantidad_personas', 'ruta', 'medio', 'alojamiento', 'precio']
        read_only_fields = ['user']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = str(instance.user)
        return rep

    def validate_titulo(self, value):
        if value.isdigit():
            raise ValidationError(MessagesES.ERROR_TITLE_TYPE)
        return value
    
    def validate_origen(self, value):
        if value.isdigit():
            raise ValidationError(MessagesES.ERROR_ORIGIN_TYPE)
        return value
    
    def validate_destino(self, value):
        if value.isdigit():
            raise ValidationError(MessagesES.ERROR_DESTINATION_TYPE)
        return value
    
    def validate_rango_fechas(self, value):
        if value.strip().isdigit():
            raise ValidationError("El rango de fechas tiene que tener el formato: AAAA-MM-DD.")
        
        patron_fechas = re.findall(r'\d{4}-\d{2}-\d{2}', value)
        
        if len(patron_fechas) == 2:
            try:
                fecha_inicio = datetime.strptime(patron_fechas[0], '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(patron_fechas[1], '%Y-%m-%d').date()
                
                if fecha_inicio > fecha_fin:
                    raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")
                
                if fecha_inicio < date.today():
                    raise ValidationError("Las fechas del viaje no pueden estar en el pasado.")
                    
            except ValueError:
                pass

        return value
    
    def validate_medio_transporte(self, value):
        if value.strip().isdigit():
            raise ValidationError("El medio de transporte no puede ser numérico.")
            
        medios_permitidos = ["TERRESTRE", "MARITIMO", "AEREA", "SIN DEFINIR", "PÚBLICO COMBINADO", "PRIVADO COMBINADO"]
        
        valor_limpio = value.strip().upper()
        
        if valor_limpio not in medios_permitidos:
            raise ValidationError(f"Medio de transporte no válido. Opciones permitidas: {', '.join(medios_permitidos)}.")
        return valor_limpio
    
    def validate_cantidad_personas(self, value):
        if value < 1:
            raise ValidationError("Debe viajar al menos 1 persona.")
        if value > 50:
            raise ValidationError("El límite máximo por consulta es de 50 personas.")
        return value

class ViajeDetailSerializer(serializers.ModelSerializer):
    ruta = RutaSerializer(read_only=True)
    medio = MedioSerializer(read_only=True)
    alojamiento = AlojamientoSerializer(read_only=True)
    user = serializers.StringRelatedField() 

    class Meta:
        model = Viaje
        fields = ['id', 'titulo', 'user', 'origen', 'destino', 'rango_fechas', 'cantidad_personas', 'ruta', 'medio', 'alojamiento', 'precio']