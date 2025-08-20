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
        if serializer.is_valid():
            plan = generar_plan_viaje(serializer.validated_data)
            
            print("Elija una de las 3 opciones de rutas:\n", plan['contenido']['rutas'])
            elecionRuta = input()
            if elecionRuta == "1":
                ruta = Ruta.objects.get(nombre_Ruta=plan['contenido']['rutas'][0]['nombre'])
            elif elecionRuta == "2":
                ruta = Ruta.objects.get(nombre_Ruta=plan['contenido']['rutas'][1]['nombre'])
            elif elecionRuta == "3":
                ruta = Ruta.objects.get(nombre_Ruta=plan['contenido']['rutas'][2]['nombre'])
            
            print("Elija una de las 3 opciones de medios:\n", plan['contenido']['medios_transporte'])
            eleccionMedio = input()
            if eleccionMedio == "1":
                medio = Medio.objects.get(nombre_Medio=plan['contenido']['medios_transporte'][0]['nombre'])
            elif eleccionMedio == "2":
                medio = Medio.objects.get(nombre_Medio=plan['contenido']['medios_transporte'][1]['nombre'])
            elif eleccionMedio == "3":
                medio = Medio.objects.get(nombre_Medio=plan['contenido']['medios_transporte'][2]['nombre'])
            
            serializer = ViajeSerializer(data={
                'titulo': serializer.validated_data['titulo'],
                'origen': serializer.validated_data['origen'],
                'destino': serializer.validated_data['destino'],
                'fecha_inicio': serializer.validated_data['fecha_inicio'],
                'fecha_fin': serializer.validated_data['fecha_fin'],
                'ruta': ruta,
                'medio': medio
            })
            
            #print("viaje creado: \n", serializer)
            self.perform_create(serializer)
            return Response({
                'success': True,
                'message': MessagesES.SUCCESS_CREATE_TRIP,
                'details': serializer.data,
                #'plan': plan
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