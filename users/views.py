from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User

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
    
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role')

    if not all([username, email, password]):
        if not username:
            return Response(
                {'error': 'Se requiere username.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif not email:
            return Response(
                {'error': 'Se requiere email.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif not password:
            return Response(
                {'error': 'Se requieren username, email y password.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'El nombre de usuario ya está en uso.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    
    user = User.objects.create_user(
        username=request.data.get('username'),
        email=request.data.get('email'),
        password=request.data.get('password'),
        role=request.data.get('role')
    )
    
    if role:
        user.role = role
    user.save()

    return Response ({'message': f'Usuario creado con éxito!', 'status': status.HTTP_201_CREATED})