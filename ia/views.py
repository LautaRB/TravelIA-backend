from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PlanViajeSerializer
from .services import generar_plan_viaje
from rest_framework.exceptions import ValidationError 

class PlanViajeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PlanViajeSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        try:
            plan = generar_plan_viaje(serializer.validated_data, request.user)
            return Response(plan)

        except Exception as e:
            raise e