from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.db import transaction
from .models import Viaje
from .serializers import ViajeSerializer, PlanificarViajeSerializer
from ia.services import generar_plan_viaje
from ruta.services import crear_ruta
from medio.services import crear_medio

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
    serializer_class = ViajeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Viaje.objects.filter(user=self.request.user).order_by('-id')

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