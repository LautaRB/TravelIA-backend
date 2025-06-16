from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer
from travelia.utils.messeges import MessagesES

# Create your views here.
class ProtectedView(APIView): # clase para la autenticación
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'success': True,
            'message': f'Hola {request.user.username}, estás autenticado',
        })

@api_view(['GET'])
def landing(request):
    return Response ('Hello Landingpage!')

@api_view(['POST'])
def register(request):
    
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": MessagesES.SUCCESS_REGISTER})
    
    raise ValidationError(serializer.errors)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username:
        raise ValidationError({"username": "Este campo es requerido" if not username else None})
    elif not password:
        raise ValidationError({"password": "Este campo es requerido" if not password else None})
    
    serializer = TokenObtainPairSerializer(data={
        'username': username,
        'password': password
    })
    
    if serializer.is_valid():
        tokens = serializer.validated_data
        return Response({
            'success': True,
            'message': MessagesES.SUCCESS_LOGIN,
            'access': tokens['access'],
            'refresh': tokens['refresh']
        })
    else:
        raise ValidationError(serializer.errors)