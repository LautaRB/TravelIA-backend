from django.urls import path
from . import views

urlpatterns = [
    path('', views.register), # Ruta principal lleva al registro la primera vez
]