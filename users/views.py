from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer

# Create your views here.
class ProtectedView(APIView): # clase para la autenticación
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"success": True, "message": "Bienvenido a la API de TravelIA"})

@api_view(['GET'])
def landing(request):
    return Response ('Hello Landingpage!')

@api_view(['POST'])
def register(request):
    
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Usuario registrado con éxito"})
    
    raise ValidationError(serializer.errors)

@api_view(['POST'])
def login(request):
    return Response ('Hello Login!')