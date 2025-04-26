from django.db import models
from django.utils import timezone


class Tbl_Categoria(models.Model):
    """
    Representa una categoría de repuestos o herramientas.
    """
    # Identificador único para cada categoría (clave primaria).
    id = models.AutoField(primary_key=True)
    # Nombre de la categoría.
    Cat_nombre = models.CharField(max_length=45, blank=False)
    # Foto asociada a la categoría (ruta o URL).
    Cat_foto = models.ImageField(upload_to='categorias/', blank=True, null=True)

    def __str__(self):
        """
        Representación en forma de cadena del objeto, mostrando el nombre de la categoría.
        """
        return self.Cat_nombre


class Tbl_Repuesto(models.Model):

    class UnidadMedida(models.TextChoices):
        UNIDADES = "UNIDADES", ("UNIDADES")
        PAQUETES = "PAQUETES", ("PAQUETES")
        ROLLOS = "ROLLOS", ("ROLLOS")
        KILOS = "KILOS", ("KILOS")
        GALONES = "GALONES", ("GALONES")
        METROS = "METROS", ("METROS")
        CAJAS = "CAJAS", ("CAJAS")
        CANECA = "CANECA", ("CANECA")
        LITROS = "LITROS", ("LITROS")
        GRAMOS = "GRAMOS", ("GRAMOS")
        TONELADAS = "TONELADAS", ("TONELADAS")
        PIEZAS = "PIEZAS", ("PIEZAS")
        METROS_CUBICOS = "METROS CÚBICOS", ("METROS CÚBICOS")
        MILIMETROS = "MILÍMETROS", ("MILÍMETROS")
        CENTIMETROS = "CENTÍMETROS", ("CENTÍMETROS")
        JUEGOS = "JUEGOS", ("JUEGOS")
        CANTIDADES = "CANTIDADES", ("CANTIDADES")
        MILLARES = "MILLARES", ("MILLARES")
        TOLVAS = "TOLVAS", ("TOLVAS")
        BIDDON = "BIDDON", ("BIDDON")
        TRAMO = "TRAMO", ("TRAMO")
        CARRETE = "CARRETE", ("CARRETE")

    """
    Representa un repuesto disponible en el sistema.
    """
    # Identificador único para cada repuesto (clave primaria).
    id = models.AutoField(primary_key=True)
    # Nombre del repuesto.
    Rep_nombre = models.CharField(max_length=45, blank=False)
    # Característica 1 del repuesto.
    Rep_caracteristica1 = models.CharField(
        max_length=60, blank=False)
    # Característica 2 del repuesto (opcional).
    Rep_caracteristica2 = models.CharField(max_length=60, blank=True)
    # Marca del repuesto (opcional).
    Rep_marca = models.CharField(max_length=45, blank=True)
    # Stock inicial del repuesto.
    Rep_stock_inicial = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False)
    # Unidad de medida del repuesto.
    Rep_unidad_medida = models.CharField(
        max_length=45, choices=UnidadMedida.choices, default=UnidadMedida.UNIDADES)
    # Ubicación del repuesto.
    Rep_ubicacion = models.CharField(max_length=35, blank=False)
    # Stock mínimo permitido del repuesto.
    Rep_stock_minimo = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False)
    # Cantidad actual de stock del repuesto.
    Rep_stock = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False)
    # Costo unitario del repuesto (opcional).
    Rep_costo_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    # Costo total calculado del repuesto (unitario * cantidad) (opcional).
    Rep_costo_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    # Observaciones adicionales sobre el repuesto (opcional).
    Rep_observaciones = models.TextField(null=True, blank=True)
    # Imagen del repuesto (opcional).
    Rep_imagen = models.ImageField(upload_to='repuestos/', blank=True, null=True)
    # Relación con la categoría de este repuesto.
    Rep_categoria = models.ForeignKey(
        Tbl_Categoria, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        """
        Representación en forma de cadena del objeto, mostrando el nombre del repuesto.
        """
        return self.Rep_nombre


class Tbl_Usuario(models.Model):
    """
    Representa un usuario dentro del sistema.
    """
    # Identificador único para cada usuario (clave primaria).
    id = models.AutoField(primary_key=True)
    # Nombre(s) del usuario.
    Usu_nombres = models.CharField(max_length=45, blank=False)
    # Apellido(s) del usuario.
    Usu_apellidos = models.CharField(max_length=45, blank=False)
    # Correo electrónico del usuario (debe ser único).
    Usu_email = models.EmailField(
        max_length=60, unique=True, null=False, blank=False)
    # Teléfono del usuario (debe ser único).
    Usu_telefono = models.CharField(
        max_length=12, unique=True, blank=False)
    # Cargo o posición del usuario (opcional).
    Usu_cargo = models.CharField(max_length=45, blank=True)
    # Área en la que trabaja el usuario (opcional).
    Usu_area = models.CharField(max_length=45, blank=True)
    # Rol del usuario, representado por un valor booleano (True/False).
    Usu_rol = models.BooleanField(null=False, blank=False)
    # Foto del usuario (opcional).
    Usu_foto = models.ImageField(upload_to='usuarios/', blank=True, null=True)
    # Estado del usuario (activo/inactivo).
    Usu_estado = models.BooleanField(default=True)
    # Indica si el usuario está en línea.
    Usu_en_linea = models.BooleanField(default=False)
    # Fecha en la cual se registró el usuario
    Usu_fecha_registro = models.DateTimeField(default=timezone.now)
    # Contraseña del usuario (almacenada como texto).
    Usu_contrasena = models.CharField(max_length=255, blank=False)

    def __str__(self):
        """
        Representación en forma de cadena del objeto, mostrando el nombre completo del usuario.
        """
        return f"{self.Usu_nombres} {self.Usu_apellidos}"


class Tbl_Movimiento(models.Model):
    """
    Representa un movimiento de repuestos o herramientas (entrada o salida).
    """

    class TipoMovimiento(models.TextChoices):
        """
        Define los tipos de movimiento: Entrada o Salida.
        """
        ENTRADA = "Entrada", ("Entrada")
        SALIDA = "Salida", ("Salida")

    # Identificador único para cada movimiento (clave primaria).
    id = models.AutoField(primary_key=True)
    # Tipo de movimiento (entrada o salida).
    Mov_tipo = models.CharField(
        max_length=20, choices=TipoMovimiento.choices, default=TipoMovimiento.ENTRADA)
    # Cantidad de repuestos o herramientas movidas.
    Mov_cantidad = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False)
    # Área a la que se realiza el movimiento.
    Mov_area = models.CharField(max_length=45, blank=False)
    # Máquina de destino del movimiento.
    Mov_maquina_destino = models.CharField(max_length=45, blank=False)
    # Referencia de la compra relacionada con el movimiento (opcional).
    Mov_referencia_compra = models.CharField(max_length=60, blank=True)
    # Costo unitario del repuesto o herramienta en el movimiento (opcional).
    Mov_costo_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    # Costo total del movimiento (cantidad * costo unitario) (opcional).
    Mov_costo_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    # Motivo del movimiento (entrada o salida).
    Mov_motivo = models.TextField(null=False, blank=False)
    # Usuario que realizó el movimiento.
    Mov_usuario = models.ForeignKey(
        Tbl_Usuario, on_delete=models.CASCADE, null=False, blank=False)
    # Repuesto o herramienta involucrado en el movimiento.
    Mov_repuesto = models.ForeignKey(
        Tbl_Repuesto, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        """
        Representación en forma de cadena del objeto, mostrando el ID y tipo del movimiento.
        """
        return f"Tbl_Movimiento {self.id} - {self.tipo}"


class Tbl_Herramienta(models.Model):

    class UnidadMedida(models.TextChoices):
        UNIDADES = "UNIDADES", ("UNIDADES")
        PAQUETES = "PAQUETES", ("PAQUETES")
        ROLLOS = "ROLLOS", ("ROLLOS")
        KILOS = "KILOS", ("KILOS")
        GALONES = "GALONES", ("GALONES")
        METROS = "METROS", ("METROS")
        CAJAS = "CAJAS", ("CAJAS")
        CANECA = "CANECA", ("CANECA")
        LITROS = "LITROS", ("LITROS")
        GRAMOS = "GRAMOS", ("GRAMOS")
        TONELADAS = "TONELADAS", ("TONELADAS")
        PIEZAS = "PIEZAS", ("PIEZAS")
        METROS_CUBICOS = "METROS CÚBICOS", ("METROS CÚBICOS")
        MILIMETROS = "MILÍMETROS", ("MILÍMETROS")
        CENTIMETROS = "CENTÍMETROS", ("CENTÍMETROS")
        JUEGOS = "JUEGOS", ("JUEGOS")
        CANTIDADES = "CANTIDADES", ("CANTIDADES")
        MILLARES = "MILLARES", ("MILLARES")
        TOLVAS = "TOLVAS", ("TOLVAS")
        BIDDON = "BIDDON", ("BIDDON")
        TRAMO = "TRAMO", ("TRAMO")
        CARRETE = "CARRETE", ("CARRETE")

    """
    Representa una herramienta en el sistema.
    """
    # Identificador único para cada herramienta (clave primaria).
    id = models.AutoField(primary_key=True)
    # Nombre de la herramienta.
    Her_nombre = models.CharField(max_length=45, blank=False)
    # Característica 1 de la herramienta.
    Her_caracteristica1 = models.CharField(max_length=60, blank=False)
    # Característica 2 de la herramienta (opcional).
    Her_caracteristica2 = models.CharField(max_length=60, blank=True)
    # Marca de la herramienta (opcional).
    Her_marca = models.CharField(max_length=45, blank=True)
    # Stock inicial de la herramienta.
    Her_stock_inicial = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False)
    # Unidad de medida de la herramienta.
    Her_unidad_medida = models.CharField(
        max_length=45, choices=UnidadMedida.choices, default=UnidadMedida.UNIDADES)
    # Ubicación de la herramienta.
    Her_ubicacion = models.CharField(max_length=35, blank=False)
    # Stock mínimo permitido de la herramienta.
    Her_stock_minimo = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False)
    # Cantidad actual de stock de la herramienta.
    Her_stock = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False)
    # Costo unitario de la herramienta (opcional).
    Her_costo_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    # Costo total calculado de la herramienta (opcional).
    Her_costo_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    # Observaciones adicionales sobre la herramienta (opcional).
    Her_observaciones = models.TextField(null=True, blank=True)
    # Imagen de la herramienta (opcional).
    Her_imagen = models.ImageField(upload_to='herramientas/', blank=True, null=True)
    # Relación con la categoría de esta herramienta.
    Her_categoria = models.ForeignKey(
        Tbl_Categoria, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        """
        Representación en forma de cadena del objeto, mostrando el nombre de la herramienta.
        """
        return self.Her_nombre


class Tbl_Prestamo(models.Model):
    """
    Representa un préstamo de herramienta.
    """
    # Identificador único para cada préstamo (clave primaria).
    id = models.AutoField(primary_key=True)
    # Cantidad de herramientas prestadas.
    Pre_cantidad = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False)
    # Área a la que se realiza el préstamo.
    Pre_area = models.CharField(max_length=45, blank=False)
    # Máquina asociada al préstamo.
    Pre_maquina = models.CharField(max_length=60, blank=False)
    # Motivo del préstamo.
    Pre_motivo_prestamo = models.TextField(null=False, blank=False)
    # Fecha de solicitud del préstamo.
    Pre_fecha_solicitud = models.DateTimeField(
        auto_now_add=True, null=False, blank=False)
    # Estado del préstamo (activo/inactivo).
    Pre_estado = models.BooleanField(null=False, blank=False)
    # Fecha de devolución de la herramienta (opcional).
    Pre_fecha_devolucion = models.DateTimeField(null=True, blank=True)
    # ID del usuario que solicita el préstamo.
    Pre_usuario_solicita = models.IntegerField(
        null=False, blank=False)
    # ID del usuario que recibe el préstamo.
    Pre_usuario_prestamo = models.IntegerField(
        null=False, blank=False)
    # Relación con la herramienta prestada.
    Pre_herramienta = models.ForeignKey(
        Tbl_Herramienta, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        """
        Representación en forma de cadena del objeto, mostrando el ID y el solicitante del préstamo.
        """
        return f"Tbl_Préstamo {self.id} - {self.Pre_usuario_solicitante}"


class Tbl_Mensaje(models.Model):
    """
    Representa un mensaje entre usuarios dentro del sistema.
    """
    # Identificador único para cada mensaje (clave primaria).
    id = models.AutoField(primary_key=True)
    # Contenido del mensaje.
    Men_contenido = models.CharField(max_length=255, blank=False)
    # Fecha de envío del mensaje.
    Men_fecha_enviado = models.DateTimeField(
        auto_now_add=True, null=False, blank=False)
    # Fecha en la que el mensaje fue leído (opcional).
    Men_fecha_leido = models.DateTimeField(null=True, blank=True)
    # Tipo de mensaje.
    Men_tipo = models.CharField(default="", max_length=20)
    # Verificación si el contenido del mensaje es una imagen.
    Men_imagen = models.BooleanField(default=False)
    # Indica si el emisor del mensaje debe eliminarlo.
    Men_eliminar_emisor = models.BooleanField(
        default=False)
    # Indica si el receptor del mensaje debe eliminarlo.
    Men_eliminar_receptor = models.BooleanField(
        default=False)
    # ID del usuario emisor del mensaje.
    Men_usuario_emisor = models.IntegerField(
        null=False, blank=False)
    # ID del usuario receptor del mensaje.
    Men_usuario_receptor = models.IntegerField(
        null=False, blank=False)

    def __str__(self):
        """
        Representación en forma de cadena del objeto, mostrando el emisor y receptor del mensaje.
        """
        return f"Mensaje de {self.Men_usuario_emisor} a {self.Men_usuario_receptor}"

class Tbl_Token(models.Model):
    usuario = models.OneToOneField(Tbl_Usuario, on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=255, unique=True)
    creado = models.DateTimeField(auto_now_add=True)

class TokenRecuperacion(models.Model):
    """
    Modelo que guarda los tokens de recuperación de contraseña generados para los usuarios.
    """
    usuario = models.ForeignKey(Tbl_Usuario, on_delete=models.CASCADE, related_name="tokens")
    token = models.CharField(max_length=255, unique=True)  # Token único
    created_at = models.DateTimeField(default=timezone.now)  # Fecha de creación del token

    def __str__(self):
        return f"Token de recuperación para {self.usuario.Usu_email} - {self.token}"

    def is_expired(self):
        """
        Método que verifica si el token ha expirado (más de 24 horas).
        """
        return self.created_at + timezone.timedelta(hours=24) < timezone.now()
