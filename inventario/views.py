from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from inventario.models import *
from inventario.serializers import *
import bcrypt
from django.core.mail import EmailMessage, BadHeaderError, get_connection
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from manejo_inventario.settings import EMAIL_HOST_USER
from django.http import BadHeaderError, JsonResponse
import json
import secrets
import bcrypt
from django.http import HttpResponse
from datetime import timedelta

# Vista para gestionar las Categorías de inventario


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Tbl_Categoria.objects.all()  # Consulta a la tabla de Categorías
    serializer_class = CategoriaSerializer  # Serializador asociado a la categoría

    # Método para crear nuevos recursos. Puede manejar tanto una lista de elementos como un solo elemento.
    def create(self, request, *args, **kwargs):
        """
        Este método maneja la creación de categorías. Puede recibir datos de una sola categoría o de múltiples categorías a la vez.
        Valida los datos recibidos, los guarda en la base de datos y retorna una respuesta con los datos creados.
        """
        # Verifica si la solicitud contiene una lista de elementos.
        if isinstance(request.data, list):
            # Si es una lista, serializa múltiples objetos.
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            # Si es un solo elemento, serializa uno solo.
            serializer = self.get_serializer(data=request.data)
        # Valida los datos serializados. Si no son válidos, se lanza una excepción.
        serializer.is_valid(raise_exception=True)
        # Guarda los datos validados en la base de datos.
        self.perform_create(serializer)
        # Obtiene los encabezados de la respuesta exitosa, como el ID de los objetos creados.
        headers = self.get_success_headers(serializer.data)
        # Retorna una respuesta con los datos creados y un estado HTTP 201 (CREATED).
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Método para realizar la creación de los datos en la base de datos.
    def perform_create(self, serializer):
        """
        Guarda los datos validados en la base de datos.
        """
        serializer.save()

    # Método para actualizar recursos existentes. Puede manejar tanto una lista de elementos como un solo elemento.
    def update(self, request, *args, **kwargs):
        """
        Este método maneja las actualizaciones de recursos (categorías). Permite la actualización de un solo recurso o de múltiples.
        Si se realiza una actualización parcial, solo se modifican los campos proporcionados.
        """
        # Determina si la actualización es parcial (es decir, no se actualizan todos los campos del recurso).
        partial = kwargs.pop('partial', False)
        # Verifica si la solicitud contiene una lista de elementos.
        if isinstance(request.data, list):
            # Si es una lista, obtiene las instancias correspondientes de la base de datos.
            instances = self.get_queryset().filter(
                id__in=[item['id'] for item in request.data])
            # Serializa los datos de las instancias para actualizar.
            serializer = self.get_serializer(
                instances, data=request.data, many=True, partial=partial)
        else:
            # Si es un solo elemento, obtiene la instancia correspondiente.
            instance = self.get_object()
            # Serializa los datos de la instancia para actualizar.
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
        # Valida los datos serializados. Si no son válidos, se lanza una excepción.
        serializer.is_valid(raise_exception=True)
        # Guarda los datos actualizados en la base de datos.
        self.perform_update(serializer)
        # Retorna una respuesta con los datos actualizados.
        return Response(serializer.data)

    # Método para realizar la actualización de los datos en la base de datos.
    def perform_update(self, serializer):
        """
        Guarda los datos actualizados en la base de datos.
        """
        serializer.save()

# Vista para gestionar los Repuestos del inventario


class RepuestoViewSet(viewsets.ModelViewSet):
    queryset = Tbl_Repuesto.objects.all()  # Consulta a la tabla de Repuestos
    serializer_class = RepuestoSerializer  # Serializador asociado a los repuestos

   # Método para crear nuevos recursos. Puede manejar tanto una lista de elementos como un solo elemento.
    def create(self, request, *args, **kwargs):
        """
        Este método maneja la creación de repuestos. Puede recibir datos de una solo repuesto o de múltiples repuestos a la vez.
        Valida los datos recibidos, los guarda en la base de datos y retorna una respuesta con los datos creados.
        """
        # Verifica si la solicitud contiene una lista de elementos.
        if isinstance(request.data, list):
            # Si es una lista, serializa múltiples objetos.
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            # Si es un solo elemento, serializa uno solo.
            serializer = self.get_serializer(data=request.data)
        # Valida los datos serializados. Si no son válidos, se lanza una excepción.
        serializer.is_valid(raise_exception=True)
        # Guarda los datos validados en la base de datos.
        self.perform_create(serializer)
        # Obtiene los encabezados de la respuesta exitosa, como el ID de los objetos creados.
        headers = self.get_success_headers(serializer.data)
        # Retorna una respuesta con los datos creados y un estado HTTP 201 (CREATED).
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Método para realizar la creación de los datos en la base de datos.
    def perform_create(self, serializer):
        """
        Guarda los datos validados en la base de datos.
        """
        serializer.save()

    # Método para actualizar recursos existentes. Puede manejar tanto una lista de elementos como un solo elemento.
    def update(self, request, *args, **kwargs):
        """
        Este método maneja las actualizaciones de recursos (repuestos). Permite la actualización de un solo recurso o de múltiples.
        Si se realiza una actualización parcial, solo se modifican los campos proporcionados.
        """
        # Determina si la actualización es parcial (es decir, no se actualizan todos los campos del recurso).
        partial = kwargs.pop('partial', False)
        # Verifica si la solicitud contiene una lista de elementos.
        if isinstance(request.data, list):
            # Si es una lista, obtiene las instancias correspondientes de la base de datos.
            instances = self.get_queryset().filter(
                id__in=[item['id'] for item in request.data])
            # Serializa los datos de las instancias para actualizar.
            serializer = self.get_serializer(
                instances, data=request.data, many=True, partial=partial)
        else:
            # Si es un solo elemento, obtiene la instancia correspondiente.
            instance = self.get_object()
            # Serializa los datos de la instancia para actualizar.
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
        # Valida los datos serializados. Si no son válidos, se lanza una excepción.
        serializer.is_valid(raise_exception=True)
        # Guarda los datos actualizados en la base de datos.
        self.perform_update(serializer)
        # Retorna una respuesta con los datos actualizados.
        return Response(serializer.data)

    # Método para realizar la actualización de los datos en la base de datos.
    def perform_update(self, serializer):
        """
        Guarda los datos actualizados en la base de datos.
        """
        serializer.save()

# Vista para gestionar los Usuarios del sistema


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Tbl_Usuario.objects.all()  # Consulta a la tabla de Usuarios
    serializer_class = UsuarioSerializer  # Serializador asociado a los usuarios

    # Método para crear nuevos recursos. Puede manejar tanto una lista de elementos como un solo elemento.
    def create(self, request, *args, **kwargs):
        """
        Este método maneja la creación de usuarios. Puede recibir datos de una sola usuario o de múltiples usuarios a la vez.
        Valida los datos recibidos, los guarda en la base de datos y retorna una respuesta con los datos creados.
        """
        # Verifica si la solicitud contiene una lista de elementos.
        if isinstance(request.data, list):
            # Si es una lista, serializa múltiples objetos.
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            # Si es un solo elemento, serializa uno solo.
            serializer = self.get_serializer(data=request.data)
        # Valida los datos serializados. Si no son válidos, se lanza una excepción.
        serializer.is_valid(raise_exception=True)
        # Guarda los datos validados en la base de datos.
        self.perform_create(serializer)
        # Obtiene los encabezados de la respuesta exitosa, como el ID de los objetos creados.
        headers = self.get_success_headers(serializer.data)
        # Retorna una respuesta con los datos creados y un estado HTTP 201 (CREATED).
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Método para realizar la creación de los datos en la base de datos.
    def perform_create(self, serializer):
        """
        Guarda los datos validados en la base de datos.
        """
        serializer.save()

    # Método para actualizar recursos existentes. Puede manejar tanto una lista de elementos como un solo elemento.
    def update(self, request, *args, **kwargs):
        """
        Este método maneja las actualizaciones de recursos (usuarios). Permite la actualización de un solo recurso o de múltiples.
        Si se realiza una actualización parcial, solo se modifican los campos proporcionados.
        """
        # Determina si la actualización es parcial (es decir, no se actualizan todos los campos del recurso).
        partial = kwargs.pop('partial', False)
        # Verifica si la solicitud contiene una lista de elementos.
        if isinstance(request.data, list):
            # Si es una lista, obtiene las instancias correspondientes de la base de datos.
            instances = self.get_queryset().filter(
                id__in=[item['id'] for item in request.data])
            # Serializa los datos de las instancias para actualizar.
            serializer = self.get_serializer(
                instances, data=request.data, many=True, partial=partial)
        else:
            # Si es un solo elemento, obtiene la instancia correspondiente.
            instance = self.get_object()
            # Serializa los datos de la instancia para actualizar.
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
        # Valida los datos serializados. Si no son válidos, se lanza una excepción.
        serializer.is_valid(raise_exception=True)
        # Guarda los datos actualizados en la base de datos.
        self.perform_update(serializer)
        # Retorna una respuesta con los datos actualizados.
        return Response(serializer.data)

    # Método para realizar la actualización de los datos en la base de datos.
    def perform_update(self, serializer):
        """
        Guarda los datos actualizados en la base de datos.
        """
        serializer.save()

# Vista para gestionar los Movimientos de inventario


class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Tbl_Movimiento.objects.all()  # Consulta a la tabla de Movimientos
    # Serializador asociado a los movimientos
    serializer_class = MovimientoSerializer

    # Método para crear nuevos recursos. Puede manejar tanto una lista de elementos como un solo elemento.
    def create(self, request, *args, **kwargs):
        """
        Este método maneja la creación de movimientos. Puede recibir datos de una sola movimiento o de múltiples movimientos a la vez.
        Valida los datos recibidos, los guarda en la base de datos y retorna una respuesta con los datos creados.
        """
        # Verifica si la solicitud contiene una lista de elementos.
        if isinstance(request.data, list):
            # Si es una lista, serializa múltiples objetos.
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            # Si es un solo elemento, serializa uno solo.
            serializer = self.get_serializer(data=request.data)
        # Valida los datos serializados. Si no son válidos, se lanza una excepción.
        serializer.is_valid(raise_exception=True)
        # Guarda los datos validados en la base de datos.
        self.perform_create(serializer)
        # Obtiene los encabezados de la respuesta exitosa, como el ID de los objetos creados.
        headers = self.get_success_headers(serializer.data)
        # Retorna una respuesta con los datos creados y un estado HTTP 201 (CREATED).
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Método para realizar la creación de los datos en la base de datos.
    def perform_create(self, serializer):
        """
        Guarda los datos validados en la base de datos.
        """
        serializer.save()

    # Método para actualizar recursos existentes. Puede manejar tanto una lista de elementos como un solo elemento.
    def update(self, request, *args, **kwargs):
        """
        Este método maneja las actualizaciones de recursos (movimientos). Permite la actualización de un solo recurso o de múltiples.
        Si se realiza una actualización parcial, solo se modifican los campos proporcionados.
        """
        # Determina si la actualización es parcial (es decir, no se actualizan todos los campos del recurso).
        partial = kwargs.pop('partial', False)
        # Verifica si la solicitud contiene una lista de elementos.
        if isinstance(request.data, list):
            # Si es una lista, obtiene las instancias correspondientes de la base de datos.
            instances = self.get_queryset().filter(
                id__in=[item['id'] for item in request.data])
            # Serializa los datos de las instancias para actualizar.
            serializer = self.get_serializer(
                instances, data=request.data, many=True, partial=partial)
        else:
            # Si es un solo elemento, obtiene la instancia correspondiente.
            instance = self.get_object()
            # Serializa los datos de la instancia para actualizar.
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
        # Valida los datos serializados. Si no son válidos, se lanza una excepción.
        serializer.is_valid(raise_exception=True)
        # Guarda los datos actualizados en la base de datos.
        self.perform_update(serializer)
        # Retorna una respuesta con los datos actualizados.
        return Response(serializer.data)

    # Método para realizar la actualización de los datos en la base de datos.
    def perform_update(self, serializer):
        """
        Guarda los datos actualizados en la base de datos.
        """
        serializer.save()

# Vista para gestionar las Herramientas de inventario


class HerramientaViewSet(viewsets.ModelViewSet):
    queryset = Tbl_Herramienta.objects.all()  # Consulta a la tabla de Herramientas
    # Serializador asociado a las herramientas
    serializer_class = HerramientaSerializer

    # Método para crear nuevos recursos. Puede manejar tanto una lista de elementos como un solo elemento.
    def create(self, request, *args, **kwargs):
        """
        Este método maneja la creación de herramientas. Puede recibir datos de una sola herramienta o de múltiples herramientas a la vez.
        Valida los datos recibidos, los guarda en la base de datos y retorna una respuesta con los datos creados.
        """
        # Verifica si la solicitud contiene una lista de elementos.
        if isinstance(request.data, list):
            # Si es una lista, serializa múltiples objetos.
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            # Si es un solo elemento, serializa uno solo.
            serializer = self.get_serializer(data=request.data)
        # Valida los datos serializados. Si no son válidos, se lanza una excepción.
        serializer.is_valid(raise_exception=True)
        # Guarda los datos validados en la base de datos.
        self.perform_create(serializer)
        # Obtiene los encabezados de la respuesta exitosa, como el ID de los objetos creados.
        headers = self.get_success_headers(serializer.data)
        # Retorna una respuesta con los datos creados y un estado HTTP 201 (CREATED).
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Método para realizar la creación de los datos en la base de datos.
    def perform_create(self, serializer):
        """
        Guarda los datos validados en la base de datos.
        """
        serializer.save()

    # Método para actualizar recursos existentes. Puede manejar tanto una lista de elementos como un solo elemento.
    def update(self, request, *args, **kwargs):
        """
        Este método maneja las actualizaciones de recursos (herramientas). Permite la actualización de un solo recurso o de múltiples.
        Si se realiza una actualización parcial, solo se modifican los campos proporcionados.
        """
        # Determina si la actualización es parcial (es decir, no se actualizan todos los campos del recurso).
        partial = kwargs.pop('partial', False)
        # Verifica si la solicitud contiene una lista de elementos.
        if isinstance(request.data, list):
            # Si es una lista, obtiene las instancias correspondientes de la base de datos.
            instances = self.get_queryset().filter(
                id__in=[item['id'] for item in request.data])
            # Serializa los datos de las instancias para actualizar.
            serializer = self.get_serializer(
                instances, data=request.data, many=True, partial=partial)
        else:
            # Si es un solo elemento, obtiene la instancia correspondiente.
            instance = self.get_object()
            # Serializa los datos de la instancia para actualizar.
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
        # Valida los datos serializados. Si no son válidos, se lanza una excepción.
        serializer.is_valid(raise_exception=True)
        # Guarda los datos actualizados en la base de datos.
        self.perform_update(serializer)
        # Retorna una respuesta con los datos actualizados.
        return Response(serializer.data)

    # Método para realizar la actualización de los datos en la base de datos.
    def perform_update(self, serializer):
        """
        Guarda los datos actualizados en la base de datos.
        """
        serializer.save()

# Vista para gestionar los Prestamos de herramientas


class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Tbl_Prestamo.objects.all()  # Consulta a la tabla de Prestamos
    serializer_class = PrestamoSerializer  # Serializador asociado a los prestamos

    # Método para crear nuevos recursos. Puede manejar tanto una lista de elementos como un solo elemento.
    def create(self, request, *args, **kwargs):
        """
        Este método maneja la creación de prestamos. Puede recibir datos de una sola prestamo o de múltiples prestamos a la vez.
        Valida los datos recibidos, los guarda en la base de datos y retorna una respuesta con los datos creados.
        """
        # Verifica si la solicitud contiene una lista de elementos.
        if isinstance(request.data, list):
            # Si es una lista, serializa múltiples objetos.
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            # Si es un solo elemento, serializa uno solo.
            serializer = self.get_serializer(data=request.data)
        # Valida los datos serializados. Si no son válidos, se lanza una excepción.
        serializer.is_valid(raise_exception=True)
        # Guarda los datos validados en la base de datos.
        self.perform_create(serializer)
        # Obtiene los encabezados de la respuesta exitosa, como el ID de los objetos creados.
        headers = self.get_success_headers(serializer.data)
        # Retorna una respuesta con los datos creados y un estado HTTP 201 (CREATED).
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Método para realizar la creación de los datos en la base de datos.
    def perform_create(self, serializer):
        """
        Guarda los datos validados en la base de datos.
        """
        serializer.save()

    # Método para actualizar recursos existentes. Puede manejar tanto una lista de elementos como un solo elemento.
    def update(self, request, *args, **kwargs):
        """
        Este método maneja las actualizaciones de recursos (prestamos). Permite la actualización de un solo recurso o de múltiples.
        Si se realiza una actualización parcial, solo se modifican los campos proporcionados.
        """
        # Determina si la actualización es parcial (es decir, no se actualizan todos los campos del recurso).
        partial = kwargs.pop('partial', False)
        # Verifica si la solicitud contiene una lista de elementos.
        if isinstance(request.data, list):
            # Si es una lista, obtiene las instancias correspondientes de la base de datos.
            instances = self.get_queryset().filter(
                id__in=[item['id'] for item in request.data])
            # Serializa los datos de las instancias para actualizar.
            serializer = self.get_serializer(
                instances, data=request.data, many=True, partial=partial)
        else:
            # Si es un solo elemento, obtiene la instancia correspondiente.
            instance = self.get_object()
            # Serializa los datos de la instancia para actualizar.
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
        # Valida los datos serializados. Si no son válidos, se lanza una excepción.
        serializer.is_valid(raise_exception=True)
        # Guarda los datos actualizados en la base de datos.
        self.perform_update(serializer)
        # Retorna una respuesta con los datos actualizados.
        return Response(serializer.data)

    # Método para realizar la actualización de los datos en la base de datos.
    def perform_update(self, serializer):
        """
        Guarda los datos actualizados en la base de datos.
        """
        serializer.save()

# Vista para gestionar los Mensajes entre usuarios


class MensajeViewSet(viewsets.ModelViewSet):
    queryset = Tbl_Mensaje.objects.all()  # Consulta a la tabla de Mensajes
    serializer_class = MensajeSerializer  # Serializador asociado a los mensajes

    # Método para crear nuevos recursos. Puede manejar tanto una lista de elementos como un solo elemento.
    def create(self, request, *args, **kwargs):
        """
        Este método maneja la creación de mensajes. Puede recibir datos de una sola mensaje o de múltiples mensajes a la vez.
        Valida los datos recibidos, los guarda en la base de datos y retorna una respuesta con los datos creados.
        """
        # Verifica si la solicitud contiene una lista de elementos.
        if isinstance(request.data, list):
            # Si es una lista, serializa múltiples objetos.
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            # Si es un solo elemento, serializa uno solo.
            serializer = self.get_serializer(data=request.data)
        # Valida los datos serializados. Si no son válidos, se lanza una excepción.
        serializer.is_valid(raise_exception=True)
        # Guarda los datos validados en la base de datos.
        self.perform_create(serializer)
        # Obtiene los encabezados de la respuesta exitosa, como el ID de los objetos creados.
        headers = self.get_success_headers(serializer.data)
        # Retorna una respuesta con los datos creados y un estado HTTP 201 (CREATED).
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Método para realizar la creación de los datos en la base de datos.
    def perform_create(self, serializer):
        """
        Guarda los datos validados en la base de datos.
        """
        serializer.save()

    # Método para actualizar recursos existentes. Puede manejar tanto una lista de elementos como un solo elemento.
    def update(self, request, *args, **kwargs):
        """
        Este método maneja las actualizaciones de recursos (mensajes). Permite la actualización de un solo recurso o de múltiples.
        Si se realiza una actualización parcial, solo se modifican los campos proporcionados.
        """
        # Determina si la actualización es parcial (es decir, no se actualizan todos los campos del recurso).
        partial = kwargs.pop('partial', False)
        # Verifica si la solicitud contiene una lista de elementos.
        if isinstance(request.data, list):
            # Si es una lista, obtiene las instancias correspondientes de la base de datos.
            instances = self.get_queryset().filter(
                id__in=[item['id'] for item in request.data])
            # Serializa los datos de las instancias para actualizar.
            serializer = self.get_serializer(
                instances, data=request.data, many=True, partial=partial)
        else:
            # Si es un solo elemento, obtiene la instancia correspondiente.
            instance = self.get_object()
            # Serializa los datos de la instancia para actualizar.
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
        # Valida los datos serializados. Si no son válidos, se lanza una excepción.
        serializer.is_valid(raise_exception=True)
        # Guarda los datos actualizados en la base de datos.
        self.perform_update(serializer)
        # Retorna una respuesta con los datos actualizados.
        return Response(serializer.data)

    # Método para realizar la actualización de los datos en la base de datos.
    def perform_update(self, serializer):
        """
        Guarda los datos actualizados en la base de datos.
        """
        serializer.save()


@api_view(['POST'])
def encriptar_password(request):
    try:
        password = request.data.get('password')
        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Generar un salt y crear el hash
        salt = bcrypt.gensalt(rounds=10)  # Genera un salt
        hashed_password = bcrypt.hashpw(password.encode(
            'utf-8'), salt).decode('utf-8')  # Hash con bcrypt

        return Response({"hashed_password": hashed_password}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def verificar_password(request):
    try:
        contrasena_ingresada = request.data.get('password')
        hash_guardado = request.data.get('hashed_password')

        if not contrasena_ingresada or not hash_guardado:
            return Response({"error": "Both 'password' and 'hashed_password' are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si la contraseña coincide con el hash guardado
        es_valida = bcrypt.checkpw(contrasena_ingresada.encode(
            'utf-8'), hash_guardado.encode('utf-8'))

        return Response({"es_valida": es_valida}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt  # Exenta esta vista de la verificación CSRF
def send_code(request):
    if request.method == 'POST':  # Verifica si el método de la solicitud es POST
        try:
            # Intenta cargar los datos JSON del cuerpo de la solicitud
            data = json.loads(request.body)
            subject = data.get("subject", "")  # Obtiene el asunto del correo
            message = data.get("message", "")  # Obtiene el mensaje del correo
            from_email = EMAIL_HOST_USER  # Dirección de correo del remitente
            # Lista de destinatarios
            recipient_list = data.get("recipient_list", "")

            # Verifica que todos los campos requeridos estén presentes
            if subject and message and from_email and recipient_list:
                try:
                    # Renderiza la plantilla HTML con el contexto
                    html_message = render_to_string('code.html', {
                        'subject': subject,
                        'message': message,
                    })

                    # Prepara el mensaje de correo
                    email = EmailMessage(
                        subject,
                        html_message,
                        from_email,
                        recipient_list.split(),  # Convierte la lista de destinatarios a una lista de Python
                        connection=get_connection()  # Obtiene la conexión de correo
                    )
                    email.content_subtype = 'html'  # Define el tipo de contenido como HTML
                    email.send()  # Envía el correo electrónico
                    return JsonResponse({"message": "Correo electrónico enviado exitosamente"}, status=200)
                except BadHeaderError:  # Captura errores relacionados con cabeceras de correo inválidas
                    return JsonResponse({"error": "Error al enviar correo electrónico"}, status=400)
            else:
                # Error si faltan campos
                return JsonResponse({"error": "Por favor, complete todos los campos"}, status=400)
        except json.JSONDecodeError:  # Captura errores en la decodificación del JSON
            return JsonResponse({"error": "Error al procesar la solicitud JSON"}, status=400)
    else:
        # Error si el método no es POST
        return JsonResponse({"error": "Método no permitido"}, status=405)


# Vista para enviar un correo electrónico a un destinatario para avisarle del estado de su usuario en el aplicativo.
@csrf_exempt  # Exenta esta vista de la verificación CSRF
def send_estado(request):
    if request.method == 'POST':  # Verifica si el método de la solicitud es POST
        try:
            # Intenta cargar los datos JSON del cuerpo de la solicitud
            data = json.loads(request.body)
            subject = data.get("subject", "")  # Obtiene el asunto del correo
            message = data.get("message", "")  # Obtiene el mensaje del correo
            from_email = EMAIL_HOST_USER  # Dirección de correo del remitente
            # Lista de destinatarios
            recipient_list = data.get("recipient_list", "")

            # Verifica que todos los campos requeridos estén presentes
            if subject and message and from_email and recipient_list:
                try:
                    # Renderiza la plantilla HTML con el contexto
                    html_message = render_to_string('estado.html', {
                        'subject': subject,
                        'message': message,
                    })

                    # Prepara el mensaje de correo
                    email = EmailMessage(
                        subject,
                        html_message,
                        from_email,
                        recipient_list.split(),  # Convierte la lista de destinatarios a una lista de Python
                        connection=get_connection()  # Obtiene la conexión de correo
                    )
                    email.content_subtype = 'html'  # Define el tipo de contenido como HTML
                    email.send()  # Envía el correo electrónico
                    return JsonResponse({"message": "Correo electrónico enviado exitosamente"}, status=200)
                except BadHeaderError:  # Captura errores relacionados con cabeceras de correo inválidas
                    return JsonResponse({"error": "Error al enviar correo electrónico"}, status=400)
            else:
                # Error si faltan campos
                return JsonResponse({"error": "Por favor, complete todos los campos"}, status=400)
        except json.JSONDecodeError:  # Captura errores en la decodificación del JSON
            return JsonResponse({"error": "Error al procesar la solicitud JSON"}, status=400)
    else:
        # Error si el método no es POST
        return JsonResponse({"error": "Método no permitido"}, status=405)


# Vista para enviar un correo electrónico a un destinatario para notificarle el rol de su usuario en el aplicativo.
@csrf_exempt  # Exenta esta vista de la verificación CSRF
def send_rol(request):
    if request.method == 'POST':  # Verifica si el método de la solicitud es POST
        try:
            # Intenta cargar los datos JSON del cuerpo de la solicitud
            data = json.loads(request.body)
            subject = data.get("subject", "")  # Obtiene el asunto del correo
            message = data.get("message", "")  # Obtiene el mensaje del correo
            from_email = EMAIL_HOST_USER  # Dirección de correo del remitente
            # Lista de destinatarios
            recipient_list = data.get("recipient_list", "")

            # Verifica que todos los campos requeridos estén presentes
            if subject and message and from_email and recipient_list:
                try:
                    # Renderiza la plantilla HTML con el contexto
                    html_message = render_to_string('rol.html', {
                        'subject': subject,
                        'message': message,
                    })

                    # Prepara el mensaje de correo
                    email = EmailMessage(
                        subject,
                        html_message,
                        from_email,
                        recipient_list.split(),  # Convierte la lista de destinatarios a una lista de Python
                        connection=get_connection()  # Obtiene la conexión de correo
                    )
                    email.content_subtype = 'html'  # Define el tipo de contenido como HTML
                    email.send()  # Envía el correo electrónico
                    return JsonResponse({"message": "Correo electrónico enviado exitosamente"}, status=200)
                except BadHeaderError:  # Captura errores relacionados con cabeceras de correo inválidas
                    return JsonResponse({"error": "Error al enviar correo electrónico"}, status=400)
            else:
                # Error si faltan campos
                return JsonResponse({"error": "Por favor, complete todos los campos"}, status=400)
        except json.JSONDecodeError:  # Captura errores en la decodificación del JSON
            return JsonResponse({"error": "Error al procesar la solicitud JSON"}, status=400)
    else:
        # Error si el método no es POST
        return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def send_contrasena(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            subject = data.get("subject", "")
            message = data.get("message", "")
            from_email = EMAIL_HOST_USER
            recipient_list = data.get("recipient_list", "")

            if subject and message and from_email and recipient_list:
                usuario = Tbl_Usuario.objects.get(Usu_email=recipient_list)

                # Verificar si ya hay un token no expirado
                token_existente = TokenRecuperacion.objects.filter(
                    usuario=usuario).order_by('-created_at').first()

                if token_existente and not token_existente.is_expired():
                    return JsonResponse({"message": "Ya se ha enviado un correo recientemente. Intente más tarde."}, status=220)

                # Si no hay token válido, se crea uno nuevo
                raw_token = secrets.token_urlsafe(32)
                token = TokenRecuperacion.objects.create(
                    usuario=usuario, token=raw_token)
                tokenUsuario = token.token
                message_con_token = f"{message}{tokenUsuario}/"

                html_message = render_to_string('contrasena.html', {
                    'subject': subject,
                    'message': message_con_token,
                })

                email = EmailMessage(
                    subject,
                    html_message,
                    from_email,
                    recipient_list.split(),
                )
                email.content_subtype = 'html'
                email.send()

                return JsonResponse({"message": "Correo electrónico enviado exitosamente"}, status=200)
            else:
                return JsonResponse({"error": "Por favor, complete todos los campos"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al procesar la solicitud JSON"}, status=400)
        except Tbl_Usuario.DoesNotExist:
            return JsonResponse({"error": "El usuario no existe"}, status=404)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)


@api_view(['POST'])
def login_usuario(request):
    email = request.data.get('email')
    # Este ya es el hash de la contraseña
    password = request.data.get('password')

    try:
        # Buscar el usuario por email
        usuario = Tbl_Usuario.objects.get(Usu_email=email)

        # Obtener el hash de la contraseña guardado
        hash_guardado = usuario.Usu_contrasena

        # Verificar si el hash enviado coincide con el hash guardado
        if password == hash_guardado:
            # Generar token aleatorio
            raw_token = secrets.token_urlsafe(32)

            # Hashear el token con bcrypt
            salt = bcrypt.gensalt(rounds=10)
            hashed_token = bcrypt.hashpw(
                raw_token.encode('utf-8'), salt).decode('utf-8')

            # Guardar el hash del token
            Tbl_Token.objects.update_or_create(
                usuario=usuario,
                defaults={'token_hash': hashed_token}
            )

            # Marcar al usuario como en línea
            usuario.Usu_en_linea = True
            usuario.save()

            # Responder con los datos del usuario y el token
            return Response({
                "usuario": UsuarioSerializer(usuario).data,
                "token": raw_token  # Este lo guarda el frontend
            }, status=200)

        # Si el hash no coincide
        return Response({"error": "Credenciales inválidas"}, status=401)

    except Tbl_Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
def logout_usuario(request):
    token = request.data.get('token')

    if not token:
        return Response({"error": "Token requerido"}, status=400)

    # Buscar todos los tokens
    tokens = Tbl_Token.objects.all()
    for t in tokens:
        if bcrypt.checkpw(token.encode('utf-8'), t.token_hash.encode('utf-8')):
            usuario = t.usuario
            t.delete()
            usuario.Usu_en_linea = False
            usuario.save()
            return Response({"message": "Sesión cerrada correctamente"}, status=200)

    return Response({"error": "Token no válido"}, status=404)


def cambiar_contrasena(request, token):
    """
    Vista para cambiar la contraseña del usuario utilizando el token.
    """
    try:
        # Buscar el token
        token_obj = get_object_or_404(TokenRecuperacion, token=token)
        usuario = token_obj.usuario

        # Verificar si el token ha expirado (24 horas)
        if token_obj.created_at + timedelta(hours=24) < timezone.now():
            return render(request, 'error.html')

        if request.method == 'POST':
            nueva_contrasena = request.POST.get('nueva_contrasena')
            confirmar_contrasena = request.POST.get('confirmar_contrasena')

            if nueva_contrasena != confirmar_contrasena:
                return render(request, 'error.html')

            # Encriptar la nueva contraseña
            salt = bcrypt.gensalt(rounds=10)
            hashed_password = bcrypt.hashpw(
                nueva_contrasena.encode('utf-8'), salt).decode('utf-8')

            # Guardar la nueva contraseña en el usuario
            usuario.Usu_contrasena = hashed_password
            usuario.save()

            # Mostrar éxito
            return render(request, 'exito.html')

        return render(request, 'cambiar_contrasena.html', {'usuario': usuario})

    except Exception as e:
        print(e)
        return render(request, 'error.html')
