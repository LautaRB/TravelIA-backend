from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import UserSerializer
from .models import User

# Create your views here.
@api_view(['GET'])
def landing(request):
    return Response ('Hello Landingpage!')

@api_view(['POST'])
def register(request):
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()
        
        token = Token.objects.create(user=user)
        
        return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
