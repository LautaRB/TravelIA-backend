import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import permissions
from django.db import transaction
from .models import Viaje
from .serializers import ViajeSerializer, ViajeDetailSerializer, PlanificarViajeSerializer
from ia.services import generar_plan_viaje
from ruta.services import crear_ruta
from medio.services import crear_medio
from alojamiento.services import crear_alojamiento
from travelia.utils.messeges import MessagesES

logger = logging.getLogger(__name__)

class PlanificarViajeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PlanificarViajeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Error en los datos enviados.',
                'errores': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            plan = generar_plan_viaje(serializer.validated_data, request.user)
            
            opciones = plan.get('contenido', {}).get('opciones', []) if isinstance(plan.get('contenido'), dict) else plan.get('contenido', [])
            
            return Response({
                'success': True,
                'message': 'Opciones generadas con éxito',
                'opciones': opciones
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error en PlanificarViajeView al llamar a la IA: {str(e)}", exc_info=True)
            
            return Response({
                'success': False,
                'message': 'Hubo un problema al generar el viaje con la IA. Por favor, intentá de nuevo.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ViajeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Viaje.objects.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ViajeDetailSerializer
        return ViajeSerializer
    
    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            data = request.data.copy()
            ruta_data = data.pop('ruta_data', None)
            if ruta_data:
                datos_para_servicio = {
                    "nombre_Ruta": ruta_data.get('nombre'),
                    "origen": data.get('origen'),
                    "destino": data.get('destino'),
                    "distancia": ruta_data.get('distancia'),
                    "tiempo": ruta_data.get('duracion_horas')
                }
                nueva_ruta, _ = crear_ruta(datos_para_servicio) 
                data['ruta'] = nueva_ruta.id

            medio_data = data.pop('medio_data', None)
            if medio_data:
                datos_para_servicio_medio = {
                    "nombre_Medio": medio_data.get('nombre'),
                    "tipo": medio_data.get('tipo'),
                    "plataforma_recomendada": medio_data.get('plataforma_recomendada')
                }
                nuevo_medio, _ = crear_medio(datos_para_servicio_medio)
                data['medio'] = nuevo_medio.id
                
                if 'precio_total' in medio_data:
                    data['precio'] = medio_data['precio_total']
                elif 'precio' in medio_data:
                    data['precio'] = medio_data['precio']
            
            alojamiento_data = data.pop('alojamiento_data', None)
            if alojamiento_data:
                datos_alojamiento = {
                    "tipo_sugerido": alojamiento_data.get('tipo_sugerido'),
                    "plataforma_recomendada": alojamiento_data.get('plataforma_recomendada')
                }
                nuevo_alojamiento, _ = crear_alojamiento(datos_alojamiento)
                data['alojamiento'] = nuevo_alojamiento.id

            data['user'] = request.user.id 
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            headers = self.get_success_headers(serializer.data)
            return Response({
                "success": True,
                "message": "Viaje guardado con éxito",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
            
    def perform_update(self, serializer):
        instance = self.get_object()
        nuevos_datos = serializer.validated_data
        
        nuevo_origen = nuevos_datos.get('origen', instance.origen)
        nuevo_destino = nuevos_datos.get('destino', instance.destino)
        
        nuevo_rango_fechas = nuevos_datos.get('rango_fechas', instance.rango_fechas)
        nueva_cantidad_personas = nuevos_datos.get('cantidad_personas', instance.cantidad_personas)

        lugares_cambiaron = (nuevo_origen != instance.origen) or (nuevo_destino != instance.destino)
        detalles_cambiaron = (nuevo_rango_fechas != instance.rango_fechas) or (nueva_cantidad_personas != instance.cantidad_personas)

        if lugares_cambiaron or detalles_cambiaron:
            serializer.save(ruta=None, medio=None, alojamiento=None, precio=None)
            
            medio_actual = instance.medio.tipo if instance.medio else "SIN DEFINIR"
            medio_transporte = self.request.data.get('medio_transporte', medio_actual)
            
            datos_para_ia = {
                "origen": nuevo_origen,
                "destino": nuevo_destino,
                "rango_fechas": nuevo_rango_fechas,
                "cantidad_personas": nueva_cantidad_personas,
                "medio_transporte": medio_transporte
            }

            try:
                plan_actualizado = generar_plan_viaje(datos_para_ia, self.request.user)
                opciones = plan_actualizado.get('contenido', {}).get('opciones', [])

                if not opciones:
                    raise ValueError("La IA no generó opciones válidas.")

                mejor_opcion = opciones[0]
                ruta_json = mejor_opcion['ruta']
                medio_json = mejor_opcion['medio']
                
                alojamiento_json = mejor_opcion.get('alojamiento')

                datos_ruta = {
                    "nombre_Ruta": ruta_json.get('nombre'),
                    "origen": nuevo_origen,
                    "destino": nuevo_destino,
                    "distancia": ruta_json.get('distancia'),
                    "tiempo": ruta_json.get('duracion_horas')
                }
                nueva_ruta_obj, _ = crear_ruta(datos_ruta)

                datos_medio = {
                    "nombre_Medio": medio_json.get('nombre'),
                    "tipo": medio_json.get('tipo'),
                    "plataforma_recomendada": medio_json.get('plataforma_recomendada')
                }
                nuevo_medio_obj, _ = crear_medio(datos_medio)
                
                nuevo_alojamiento_obj = None
                if alojamiento_json:
                    datos_alojamiento = {
                        "tipo_sugerido": alojamiento_json.get('tipo_sugerido'),
                        "plataforma_recomendada": alojamiento_json.get('plataforma_recomendada')
                    }
                    nuevo_alojamiento_obj, _ = crear_alojamiento(datos_alojamiento)

                instance.refresh_from_db()
                instance.ruta = nueva_ruta_obj
                instance.medio = nuevo_medio_obj
                
                if nuevo_alojamiento_obj:
                    instance.alojamiento = nuevo_alojamiento_obj
                
                precio_sugerido = medio_json.get('precio_total')
                if precio_sugerido:
                    instance.precio = precio_sugerido
                
                instance.save()

            except Exception as e:
                logger.error(f"Error crítico recalculando viaje ID {instance.id}: {str(e)}", exc_info=True)
                raise ValidationError(MessagesES.ERROR_UPDATE_TRIP)

        else:
            serializer.save()