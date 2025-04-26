from django.contrib import admin
from .models import Tbl_Usuario, Tbl_Categoria, Tbl_Herramienta, Tbl_Repuesto, Tbl_Prestamo, Tbl_Movimiento, Tbl_Mensaje

# Register your models here.

# Registra el modelo Tbl_Categoria en el panel de administración de Django.
# Esto permitirá gestionar las categorías de repuestos y herramientas.
admin.site.register(Tbl_Categoria)
# Registra el modelo Tbl_Repuesto en el panel de administración de Django.
# Esto permitirá gestionar los repuestos disponibles en el sistema.
admin.site.register(Tbl_Repuesto)
# Registra el modelo Tbl_Usuario en el panel de administración de Django.
# Esto permitirá gestionar los usuarios a través de la interfaz administrativa.
admin.site.register(Tbl_Usuario)
# Registra el modelo Tbl_Movimiento en el panel de administración de Django.
# Esto permitirá gestionar los movimientos de repuestos o herramientas (entradas y salidas).
admin.site.register(Tbl_Movimiento)
# Registra el modelo Tbl_Categoria en el panel de administración de Django.
# Esto permitirá gestionar las categorías de repuestos y herramientas.
admin.site.register(Tbl_Herramienta)
# Registra el modelo Tbl_Prestamo en el panel de administración de Django.
# Esto permitirá gestionar los préstamos de herramientas a través de la interfaz administrativa.
admin.site.register(Tbl_Prestamo)
# Registra el modelo Tbl_Mensaje en el panel de administración de Django.
# Esto permitirá gestionar los mensajes enviados entre usuarios a través de la interfaz administrativa.
admin.site.register(Tbl_Mensaje)
