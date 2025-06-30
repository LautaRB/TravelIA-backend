from rest_framework import viewsets
from travelia.utils.permissions import IsAdminOrReadOnly
from .models import Medio
from .serializers import MedioSerializer

# Create your views here.
class MedioViewSet(viewsets.ModelViewSet):
    queryset = Medio.objects.all()
    serializer_class = MedioSerializer
    # Sólo STAFF (superuser) puede crear/editar/eliminar medios
    permission_classes = [IsAdminOrReadOnly]