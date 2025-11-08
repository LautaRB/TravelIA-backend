from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from travelia.utils.messeges import MessagesES
from django.contrib.auth import get_user_model
from firebase_admin import auth
from firebase_admin._auth_utils import InvalidIdTokenError

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
def firebase_login(request): #Google Login
    try:
        token = request.data.get("token")

        if not token:
            return Response(
                {"success": False, "message": "Falta token de Firebase"},
                status=400
            )

        decoded_token = auth.verify_id_token(token)
        uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        username = decoded_token.get("name") or email.split("@")[0]
        picture = decoded_token.get("picture")

        if not email:
            return Response(
                {"success": False, "message": "El token de Firebase no contiene email válido"},
                status=400
            )

        user, created = User.objects.get_or_create(email=email, defaults={
            "username": username,
            "profile_picture": picture if hasattr(User, "profile_picture") else None,
        })

        refresh = RefreshToken.for_user(user)

        return Response({
            "success": True,
            "message": "Login con Firebase exitoso",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "created": created,
        })

    except (InvalidIdTokenError, auth.ExpiredIdTokenError):
        return Response({
            "success": False,
            "message": "Token de Firebase inválido o expirado",
        }, status=401)

    except Exception as e:
        return Response({
            "success": False,
            "message": "Error en login con Firebase",
            "details": str(e)
        }, status=400)