from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PlanViajeSerializer
from .services import generar_plan_viaje

class PlanViajeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PlanViajeSerializer(data=request.data)
        if serializer.is_valid():
            plan = generar_plan_viaje(serializer.validated_data, request.user)
            return Response(plan)
        return Response(serializer.errors, status=400)
