from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing), #Ruta principal
    path('users/refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/protected/', views.ProtectedView.as_view(), name='protected'), #Ruta para el usuario autenticado
    path('users/register/', views.register),
    path('users/login/', views.login),
]