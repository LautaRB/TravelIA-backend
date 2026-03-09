import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.db import transaction
from .models import Viaje
from .serializers import ViajeSerializer, ViajeDetailSerializer, PlanificarViajeSerializer
from ia.services import generar_plan_viaje
from ruta.services import crear_ruta
from medio.services import crear_medio
from alojamiento.services import crear_alojamiento

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
            
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        with transaction.atomic():
            data = request.data.copy()
            
            ruta_data = data.pop('ruta_data', None)
            medio_data = data.pop('medio_data', None)
            alojamiento_data = data.pop('alojamiento_data', None)

            if ruta_data:
                datos_ruta = {
                    "nombre_Ruta": ruta_data.get('nombre'),
                    "origen": data.get('origen', instance.origen),
                    "destino": data.get('destino', instance.destino),
                    "distancia": ruta_data.get('distancia'),
                    "tiempo": ruta_data.get('duracion_horas')
                }
                nueva_ruta, _ = crear_ruta(datos_ruta)
                data['ruta'] = nueva_ruta.id

            if medio_data:
                datos_medio = {
                    "nombre_Medio": medio_data.get('nombre'),
                    "tipo": medio_data.get('tipo'),
                    "plataforma_recomendada": medio_data.get('plataforma_recomendada')
                }
                nuevo_medio, _ = crear_medio(datos_medio)
                data['medio'] = nuevo_medio.id
                
                if 'precio_total' in medio_data:
                    data['precio'] = medio_data['precio_total']
                elif 'precio' in medio_data:
                    data['precio'] = medio_data['precio']

            if alojamiento_data:
                datos_alojamiento = {
                    "tipo_sugerido": alojamiento_data.get('tipo_sugerido'),
                    "plataforma_recomendada": alojamiento_data.get('plataforma_recomendada')
                }
                nuevo_alojamiento, _ = crear_alojamiento(datos_alojamiento)
                data['alojamiento'] = nuevo_alojamiento.id

            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({
                "success": True,
                "message": "Viaje actualizado con éxito",
                "data": serializer.data
            }, status=status.HTTP_200_OK)