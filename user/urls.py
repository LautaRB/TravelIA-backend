from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/profile/', views.ProtectedView.as_view(), name='protected'), #Rutas para el usuario autenticado
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('google/', views.google_login),
]