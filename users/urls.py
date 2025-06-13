from django.urls import path
from . import views

urlpatterns = [
    path('api/users/protected/', views.ProtectedView.as_view(), name='protected'), #Ruta para el usuario autenticado
    path('', views.landing), #Ruta principal
    path('api/users/register/', views.register),
    path('api/users/login/', views.login),
]