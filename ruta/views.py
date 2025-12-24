from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from travelia.utils.messeges import MessagesES
from travelia.utils.permissions import IsAdminOrReadOnly
from .models import Ruta
from .serializers import RutaSerializer
from .services import crear_ruta

class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [IsAdminOrReadOnly]
            
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        creada = crear_ruta(serializer.validated_data)
        
        return Response({
            'success': True,
            'message': MessagesES.SUCCESS_CREATE_ROUTE if creada[1] else MessagesES.ERROR_ROUTE_EXISTS,
            'details': serializer.data
        }, status=status.HTTP_201_CREATED if creada[1] else status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        serializer.is_valid(raise_exception=True)
        
        self.perform_update(serializer)
        
        return Response({
            'success': True,
            'message': MessagesES.SUCCESS_UPDATE_ROUTE,
            'details': serializer.data
        }, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({
            'success': True,
            'message': MessagesES.SUCCESS_DELETE_ROUTE
        }, status=status.HTTP_200_OK)