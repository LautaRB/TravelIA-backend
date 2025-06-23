from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing), #Ruta principal
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/profile/', views.ProtectedView.as_view(), name='protected'), #Ruta para el usuario autenticado
    path('me/profile/', views.ProtectedView.as_view(), name='protected'),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
]