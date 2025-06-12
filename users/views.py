from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer

# Create your views here.
class ProtectedView(APIView): # clase para la autenticación
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hola, {request.user.username}! Estás autenticado con JWT."})

@api_view(['GET'])
def landing(request):
    return Response ('Hello Landingpage!')

@api_view(['POST'])
def register(request):
    
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': '¡Usuario registrado con éxito!'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)