from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from travelia.utils.messeges import MessagesES
from .models import Viaje
from .serializers import ViajeSerializer

# Create your views here.
class ViajeViewSet(viewsets.ModelViewSet):
    serializer_class = ViajeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Viajes del usuario autenticado
        return Viaje.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Asocia automáticamente el nuevo viaje al user logueado
        try:
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                return Response({
                    'success': True,
                    'message': MessagesES.SUCCESS_CREATE_TRIP
                })
            raise serializer.ValidationError(serializer.errors)
        except Exception as e:
            return Response({
                'success': False,
                'message': MessagesES.ERROR_CREATE_TRIP,
                'details': str(e)
            }, status=400)
    
    def perform_update(self, serializer):
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': MessagesES.SUCCESS_UPDATE_TRIP
                })
            raise serializer.ValidationError(serializer.errors)
        except Exception as e:
            return Response({
                'success': False,
                'message': MessagesES.ERROR_UPDATE_TRIP,
                'details': str(e)
            }, status=400)
            
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