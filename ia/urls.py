from django.urls import path
from .views import PlanViajeAPIView

urlpatterns = [
    path('plan-viaje/', PlanViajeAPIView.as_view(), name='plan-viaje'),
]
