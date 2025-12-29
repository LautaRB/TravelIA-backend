from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, AuthenticationFailed 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from .serializers import UserSerializer
from travelia.utils.messeges import MessagesES

User = get_user_model()

class ProtectedView(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'success': True,
            'message': 'Datos del perfil recuperados',
            'details': serializer.data
        })
    
    def patch(self, request):
        serializer = UserSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'success': True,
            'message': MessagesES.SUCCESS_MODIFY_PROFILE,
            'details': serializer.data
        })

def validar_username_manual(username):
    if not username:
        return
        
    if " " in username:
        raise ValidationError({"username": [MessagesES.ERROR_USERNAME_SPACES]})
        
    if username.isdigit():
        raise ValidationError({"username": [MessagesES.ERROR_USERNAME_TYPE]})
    
    if username in User.objects.values_list('username', flat=True):
        raise ValidationError({"username": [MessagesES.ERROR_USER_ALREADY_EXISTS]})

@api_view(['POST'])
def register(request):
    validar_username_manual(request.data.get('username'))

    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return Response({"success": True, "message": MessagesES.SUCCESS_REGISTER})

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    validar_username_manual(username)

    serializer = TokenObtainPairSerializer(data={
        'username': username,
        'password': password
    })
    
    serializer.is_valid(raise_exception=True)
    tokens = serializer.validated_data
    
    return Response({
        'success': True,
        'message': MessagesES.SUCCESS_LOGIN,
        'access': tokens['access'],
        'refresh': tokens['refresh']
    })
    
@api_view(['POST'])
def logout(request):
    refresh_token = request.data.get('refresh')
    
    if not refresh_token:
        raise ValidationError({"refresh": MessagesES.ERROR_REFRESH_REQUIRED})

    token = RefreshToken(refresh_token)
    token.blacklist()

    return Response({
        'success': True,
        'message': MessagesES.SUCCESS_LOGOUT
    })
        
@api_view(['POST'])
def firebase_login(request): 
    token = request.data.get("token")

    if not token:
        raise ValidationError("Falta token de Google")

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.WEB_CLIENT_ID)
    except ValueError as e:
        raise AuthenticationFailed(f"Token de Google inválido: {str(e)}")

    uid = idinfo['sub'] 
    email = idinfo['email']
    username = idinfo.get('name') or email.split("@")[0]
    picture = idinfo.get('picture')

    if not email:
        raise ValidationError("El token de Google no contiene un email válido")

    user, created = User.objects.get_or_create(email=email, defaults={
        "username": username,
        "google_profile_picture": picture, 
        "profile_picture": None
    })

    if not created and not user.profile_picture and not user.google_profile_picture and picture:
            user.google_profile_picture = picture
            user.save()
    
    refresh = RefreshToken.for_user(user)

    return Response({
        "success": True,
        "message": "Login con Google exitoso",
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "created": created,
    })