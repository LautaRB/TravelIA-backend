from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ProtectedView(APIView): # clase para testear la autenticación
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hola, {request.user.username}! Estás autenticado con JWT."})

@api_view(['GET'])
def landing(request):
    return Response ('Hello Landingpage!')

@api_view(['POST'])
def register(request):
    return Response ('Hello Register!')