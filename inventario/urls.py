# Importamos las librerías necesarias para manejar las URLs y vistas en Django.
from django.urls import path, include
# Importa el enrutador de Django Rest Framework para manejar las rutas de la API
from rest_framework import routers
# Importa todas las vistas desde el archivo 'views' de la aplicación 'inventario'
from inventario.views import *

# Creamos una instancia del DefaultRouter, que es una clase proporcionada por Django Rest Framework
# que se encarga de crear las rutas automáticamente para los ViewSets registrados.
router = routers.DefaultRouter()

# Registramos los diferentes ViewSets en el enrutador, lo que permite la creación automática de rutas RESTful.
# Cada línea registra una vista relacionada con los modelos de la aplicación, y define un nombre base para la ruta.
# Ruta para gestionar categorías
router.register(r'categorias', CategoriaViewSet, basename='categorias')
# Ruta para gestionar repuestos
router.register(r'repuestos', RepuestoViewSet, basename='repuestos')
# Ruta para gestionar usuarios
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
# Ruta para gestionar movimientos
router.register(r'movimientos', MovimientoViewSet, basename='movimientos')
# Ruta para gestionar herramientas
router.register(r'herramientas', HerramientaViewSet, basename='herramientas')
# Ruta para gestionar préstamos
router.register(r'prestamos', PrestamoViewSet, basename='prestamos')
# Ruta para gestionar mensajes
router.register(r'mensajes', MensajeViewSet, basename='mensajes')


# Definimos las rutas de la API que serán incluidas en el archivo de URLs de Django
urlpatterns = [
    # Incluimos todas las rutas definidas en el enrutador del API
    # Esto es equivalente a incluir las URLs de cada ViewSet registrado
    path('', include(router.urls)),
    path('encriptar/', encriptar_password, name='encriptar'),
    path('verificar/', verificar_password, name='verificar'),
    # Ruta para la vista de envío de correos electrónicos de autenticación de codigo
    path('send_code/', send_code, name='send_code'),
    # Ruta para la vista de envío de correos electrónicos de notificación de estado de usuario
    path('send_estado/', send_estado, name='send_estado'),
    # Ruta para la vista de envío de correos electrónicos de notificación de rol de usuario
    path('send_rol/', send_rol, name='send_rol'),
    path('login/', login_usuario, name='login_usuario'),
    path('logout/', logout_usuario, name='logout_usuario'),
    path('send_contrasena/', send_contrasena, name='send_contrasena'),
    path('cambiar_contrasena/<str:token>/', cambiar_contrasena, name='cambiar_contrasena'),
]

# Añadimos las URLs definidas en el router a la lista final de rutas
# Esto permite que las rutas de los ViewSets se puedan acceder a través de las URLs de la aplicación
urlpatterns += router.urls
