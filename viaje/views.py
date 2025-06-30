from rest_framework import viewsets, permissions
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
        serializer.save(user=self.request.user)