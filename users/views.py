from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from travelia.utils.messeges import MessagesES

# Create your views here.
class ProtectedView(APIView): # clase para la autenticación
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'success': True,
            'message': f'Hola {request.user.username}, estás autenticado',
            'details': {
                'username': request.user.username,
                'email': request.user.email,
                'role': request.user.role
            }
        })
    
    def patch(self, request):
        try:
            serializer = UserSerializer(instance=request.user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': MessagesES.SUCCESS_MODIFY_PROFILE
                })
            raise ValidationError(serializer.errors)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': MessagesES.ERROR_MODIFY_PROFILE,
                'details': str(e)
            }, status=400)

@api_view(['POST'])
def register(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": MessagesES.SUCCESS_REGISTER})
        raise ValidationError(serializer.errors)
    except Exception as e:
        return Response({"success": False, "message": MessagesES.ERROR_REGISTER, "details": str(e)}, status=400)

@api_view(['POST'])
def login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
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
    except Exception as e:
        return Response({"success": False, "message": MessagesES.ERROR_LOGIN, "details": str(e)}, status=400)
    
@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')

        token = RefreshToken(refresh_token)
        token.blacklist()  # Invalida el refresh token

        return Response({
            'success': True,
            'message': MessagesES.SUCCESS_LOGOUT
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': MessagesES.ERROR_LOGOUT,
            'details': str(e)
        }, status=400)