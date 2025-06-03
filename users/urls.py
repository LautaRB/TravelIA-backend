from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing), #Ruta principal
    path('register/', views.register),
]