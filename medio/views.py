from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from travelia.utils.messeges import MessagesES
from travelia.utils.permissions import IsAdminOrReadOnly
from .models import Medio
from .serializers import MedioSerializer
from .services import crear_medio

class MedioViewSet(viewsets.ModelViewSet):
    queryset = Medio.objects.all()
    serializer_class = MedioSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        creado = crear_medio(serializer.validated_data)
        
        return Response({
            'success': True,
            'message': MessagesES.SUCCESS_CREATE_MEDIA if creado[1] else MessagesES.ERROR_MEDIA_EXISTS,
            'details': serializer.data
        }, status=status.HTTP_201_CREATED if creado[1] else status.HTTP_200_OK)
    
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
            'message': MessagesES.SUCCESS_UPDATE_MEDIA,
            'details': serializer.data
        }, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({
            'success': True,
            'message': MessagesES.SUCCESS_DELETE_MEDIA
        }, status=status.HTTP_200_OK)