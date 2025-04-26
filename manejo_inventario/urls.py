"""
URL configuration for manejo_inventario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from inventario.urls import *  # Importa las rutas de la aplicación 'inventario'
from rest_framework import permissions  # Importa los permisos para la API
# Herramienta para la documentación interactiva de la API
from drf_yasg.views import get_schema_view
# Importa herramientas de especificación para la documentación Swagger
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

# Configuración de la vista de la documentación de la API utilizando 'drf_yasg'
schema_view = get_schema_view(
    openapi.Info(
        title="S.G.I.M GOYA API",  # Título de la API
        default_version='v1',  # Versión de la API
        # Descripción de la API
        description="API oficial del Sistema de Gestión de Inventarios Mantenimiento GOYA.",
        terms_of_service="https://www.google.com/policies/terms/",  # Términos de servicio
        # Información de contacto
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),  # Licencia de la API
    ),
    public=True,  # Define que la documentación es pública
    # Permite acceso sin restricciones
    permission_classes=(permissions.AllowAny,),
    # No se requiere autenticación para acceder a la documentación
    authentication_classes=[]
)

# Lista de rutas de URLs
urlpatterns = [
    # Ruta para el panel de administración de Django
    path('admin/', admin.site.urls),
    # # Incluye las rutas de la API definidas en la aplicación 'inventario'
    path('api/', include(urlpatterns)),
    # Ruta para acceder a la documentación en formato JSON
    path('documentacion.json', schema_view.without_ui(cache_timeout=0),
         name='documentacion-json'),
    # Ruta para acceder a la documentación en formato Swagger UI
    path('documentacion/', schema_view.with_ui('swagger',
         cache_timeout=0), name='documentacion'),
    # Ruta para acceder a la documentación en formato ReDoc
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
