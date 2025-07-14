from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from travelia.utils.messeges import MessagesES
from travelia.utils.permissions import IsAdminOrReadOnly
from .models import Ruta
from .serializers import RutaSerializer

# Create your views here.
class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    # Sólo STAFF (superuser) puede crear/editar/eliminar rutas 
    permission_classes = [IsAdminOrReadOnly]
    
    def perform_create (self, serializer):
        serializer.save()
            
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                'success': True,
                'message': MessagesES.SUCCESS_CREATE_ROUTE,
                'details': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'message': MessagesES.ERROR_CREATE_ROUTE,
            'details': serializer.errors
        },  status=status.HTTP_400_BAD_REQUEST)
    
    def perform_update(self, serializer):
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                'success': True,
                'message': MessagesES.SUCCESS_UPDATE_ROUTE,
                'details': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': MessagesES.ERROR_UPDATE_ROUTE,
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_destroy(self, instance):
        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'success': True,
                'message': MessagesES.SUCCESS_DELETE_ROUTE
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': MessagesES.ERROR_DELETE_ROUTE,
                'details': str(e)
            }, status=400)