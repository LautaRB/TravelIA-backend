from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from travelia.utils.exception_handler import custom_exception_handler
from .serializers import UserSerializer

# Create your views here.
class ProtectedView(APIView): # clase para la autenticación
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return custom_exception_handler(request)

@api_view(['GET'])
def landing(request):
    return Response ('Hello Landingpage!')

@api_view(['POST'])
def register(request):
    
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return custom_exception_handler(serializer.errors)
    
    return custom_exception_handler(serializer.errors)

@api_view(['POST'])
def login(request):
    return custom_exception_handler(request)