from rest_framework import viewsets, permissions
from rest_framework.response import Response
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