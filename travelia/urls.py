from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from ruta.views import RutaViewSet
from medio.views import MedioViewSet
from viaje.views import ViajeViewSet

router = DefaultRouter()
router.register(r'viajes', ViajeViewSet, basename='viaje')
router.register(r'medios', MedioViewSet, basename='medio')
router.register(r'rutas', RutaViewSet, basename='ruta')

urlpatterns = [
    path('api/', include(router.urls)), #Rutas de los viajes, medios y rutas
    path('api/admin/', admin.site.urls), # Rutas del Administrador (superuser)
    path('api/users/', include('user.urls')), # Rutas principales del usuario
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
