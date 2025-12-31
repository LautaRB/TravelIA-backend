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
from travelia.utils.messeges import MessagesES

logger = logging.getLogger(__name__)

class PlanificarViajeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PlanificarViajeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        plan = generar_plan_viaje(serializer.validated_data, request.user)
        
        return Response({
            'success': True,
            'message': 'Opciones generadas con éxito',
            'opciones': plan['contenido']
        }, status=status.HTTP_200_OK)


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
                    "tipo": medio_data.get('tipo')
                }
                
                nuevo_medio, _ = crear_medio(datos_para_servicio_medio)
                data['medio'] = nuevo_medio.id
                
                if 'precio' in medio_data:
                    data['precio'] = medio_data['precio']

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
        nueva_fecha_inicio = nuevos_datos.get('fecha_inicio', instance.fecha_inicio)
        nueva_fecha_fin = nuevos_datos.get('fecha_fin', instance.fecha_fin)

        lugares_cambiaron = (nuevo_origen != instance.origen) or (nuevo_destino != instance.destino)
        fechas_cambiaron = (nueva_fecha_inicio != instance.fecha_inicio) or (nueva_fecha_fin != instance.fecha_fin)

        if lugares_cambiaron or fechas_cambiaron:
            serializer.save(ruta=None, medio=None, precio=None)
            
            datos_para_ia = {
                "origen": nuevo_origen,
                "destino": nuevo_destino,
                "fecha_inicio": str(nueva_fecha_inicio),
                "fecha_fin": str(nueva_fecha_fin)
            }

            try:
                plan_actualizado = generar_plan_viaje(datos_para_ia, self.request.user)
                opciones = plan_actualizado.get('contenido', {}).get('opciones', [])

                if not opciones:
                    raise ValueError("La IA no generó opciones válidas.")

                mejor_opcion = opciones[0]
                ruta_json = mejor_opcion['ruta']
                medio_json = mejor_opcion['medio']

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
                    "tipo": medio_json.get('tipo')
                }
                nuevo_medio_obj, _ = crear_medio(datos_medio)

                instance.refresh_from_db()
                instance.ruta = nueva_ruta_obj
                instance.medio = nuevo_medio_obj
                
                precio_sugerido = medio_json.get('precio')
                if precio_sugerido:
                    instance.precio = precio_sugerido
                
                instance.save()

            except Exception as e:
                logger.error(f"Error crítico recalculando viaje ID {instance.id}: {str(e)}", exc_info=True)
                raise ValidationError(MessagesES.ERROR_UPDATE_TRIP)

        else:
            serializer.save()