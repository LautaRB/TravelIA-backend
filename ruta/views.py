from rest_framework import viewsets
from travelia.utils.permissions import IsAdminOrReadOnly
from .models import Ruta
from .serializers import RutaSerializer

# Create your views here.
class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    # Sólo STAFF (superuser) puede crear/editar/eliminar rutas 
    permission_classes = [IsAdminOrReadOnly]