from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from travelia.utils.messeges import MessagesES
from .models import Viaje
from ruta.models import Ruta
from medio.models import Medio
from .serializers import ViajeSerializer
from ia.services import generar_plan_viaje

# Create your views here.
class ViajeViewSet(viewsets.ModelViewSet):
    serializer_class = ViajeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Viajes del usuario autenticado
        user = self.request.user
        if user.is_superuser:
            return Viaje.objects.all()
        return Viaje.objects.filter(user=user)

    def perform_create(self, serializer):
        # Asocia automáticamente el nuevo viaje al user logueado
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan = generar_plan_viaje(serializer.validated_data)

        print("Elija una de las 3 opciones de rutas:\n", plan['contenido']['rutas'])
        eleccionRuta = input()
        ruta = Ruta.objects.get(nombre_Ruta=plan['contenido']['rutas'][int(eleccionRuta)-1]['nombre'])

        print("Elija una de las 3 opciones de medios:\n", plan['contenido']['medios'])
        eleccionMedio = input()
        medio = Medio.objects.get(nombre_Medio=plan['contenido']['medios'][int(eleccionMedio)-1]['nombre'])

        final_serializer = self.get_serializer(data={
            **serializer.validated_data,
            'ruta': ruta.id,
            'medio': medio.id
        })
        final_serializer.is_valid(raise_exception=True)
        self.perform_create(final_serializer)

        return Response({
            'success': True,
            'message': MessagesES.SUCCESS_CREATE_TRIP,
            'details': final_serializer.data,
        }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': MessagesES.ERROR_CREATE_TRIP,
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                'success': True,
                'message': MessagesES.SUCCESS_UPDATE_TRIP,
                'details': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': MessagesES.ERROR_UPDATE_TRIP,
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
            
    def perform_destroy(self, instance):
        instance.delete()
    
    def destroy(self, request, *args, **kwargs): # Para retornar una respuesta
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'success': True,
                'message': MessagesES.SUCCESS_DELETE_TRIP
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': MessagesES.ERROR_DELETE_TRIP,
                'details': str(e)
            }, status=400)