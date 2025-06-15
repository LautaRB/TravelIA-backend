from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing), #Ruta principal
    path('users/tokens/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # obtiene el par de tokens
    path('users/refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/protected/', views.ProtectedView.as_view(), name='protected'), #Ruta para el usuario autenticado
    path('users/register/', views.register),
    path('users/login/', views.login),
]