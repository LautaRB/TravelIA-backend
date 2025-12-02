from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from travelia.utils.messeges import MessagesES
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings

User = get_user_model()

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
        
@api_view(['POST'])
def firebase_login(request): # Google Login
    try:
        token = request.data.get("token")

        if not token:
            return Response(
                {"success": False, "message": "Falta token de Google"},
                status=400
            )

        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.WEB_CLIENT_ID)

        uid = idinfo['sub'] 
        email = idinfo['email']
        username = idinfo.get('name') or email.split("@")[0]
        picture = idinfo.get('picture')

        if not email:
            return Response(
                {"success": False, "message": "El token no contiene email válido"},
                status=400
            )

        user, created = User.objects.get_or_create(email=email, defaults={
            "username": username,
            "profile_picture": picture if hasattr(User, "profile_picture") else None, 
        })

        refresh = RefreshToken.for_user(user)

        return Response({
            "success": True,
            "message": "Login con Google exitoso",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "created": created,
        })

    except ValueError as e:
        print(f"Error de validación de token: {str(e)}")
        return Response({
            "success": False,
            "message": "Token inválido",
            "details": str(e)
        }, status=401)

    except Exception as e:
        return Response({
            "success": False,
            "message": "Error en login con Google",
            "details": str(e)
        }, status=400)