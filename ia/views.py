from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import generar_plan_viaje  # lógica que vos vas a definir

# Create your views here.
class PlanearViajeIA(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        datos_usuario = request.data
        respuesta_ia = generar_plan_viaje(datos_usuario, user=request.user)
        return Response(respuesta_ia)