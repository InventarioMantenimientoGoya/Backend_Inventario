# Importación de las librerías necesarias
# Librería para la serialización de datos en Django REST framework
from rest_framework import serializers
from inventario.models import *  # Importa todos los modelos del archivo 'models.py'


# Serializador para el modelo Tbl_Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    # Meta clase para especificar el modelo y los campos a serializar
    class Meta:
        model = Tbl_Categoria  # Especifica el modelo Tbl_Categoria para este serializador
        fields = '__all__'  # Serializa todos los campos del modelo, sin excepción

    # Método para crear registros de categorías de manera masiva
    def create(self, validated_data):
        """
        Este método permite crear una o más instancias del modelo Tbl_Categoria de manera masiva.
        Si se reciben varios elementos en 'validated_data' (lista), se crean todas las categorías
        de una vez. Si se recibe un solo elemento, se crea una sola categoría.
        """
        # Verificar si los datos validados son una lista de diccionarios
        if isinstance(validated_data, list):
            # Crear una instancia de Tbl_Categoria para cada diccionario de la lista
            categorias = [Tbl_Categoria(**item) for item in validated_data]
            # Guardar todas las categorías en la base de datos de una sola vez
            return Tbl_Categoria.objects.bulk_create(categorias)
        # Si no es una lista, se crea una sola instancia
        return Tbl_Categoria.objects.create(**validated_data)

    # Método para actualizar registros de categorías de manera masiva
    def update(self, instance, validated_data):

        nueva_foto = validated_data.get('Cat_foto', None)

        # 👉 Si viene una nueva foto, y ya hay una foto anterior, la borramos
        if nueva_foto and instance.Cat_foto and instance.Cat_foto != nueva_foto:
            instance.Cat_foto.delete(save=False)

        # 👉 Si se quiere eliminar la foto (null), y hay una foto, también la borramos
        if 'Cat_foto' in validated_data and validated_data['Cat_foto'] is None:
            if instance.Cat_foto:
                instance.Cat_foto.delete(save=False)

        """
        Este método actualiza registros existentes de Tbl_Categoria. Si 'validated_data' es una lista,
        actualiza varias instancias basándose en el ID de cada categoría. Si es un solo objeto,
        actualiza solo ese registro.
        """
        # Verificar si los datos validados son una lista de diccionarios
        if isinstance(validated_data, list):
            # Crear un diccionario que mapea los IDs de las categorías existentes a sus instancias
            categoria_mapping = {
                categoria.id: categoria for categoria in instance}
            # Lista para almacenar las categorías actualizadas
            ret = []

            # Iterar sobre cada elemento en la lista de datos validados para actualizar cada categoría
            for item in validated_data:
                # Obtener la categoría correspondiente por ID
                categoria = categoria_mapping.get(item.get('id'))
                # Actualizar los atributos de la categoría con los nuevos valores de 'item'
                for attr, value in item.items():
                    setattr(categoria, attr, value)
                # Guardar los cambios en la base de datos
                categoria.save()
                # Agregar la categoría actualizada a la lista
                ret.append(categoria)

            # Devolver la lista de categorías actualizadas
            return ret
        # Si no es una lista, actualizar solo una categoría
        return super().update(instance, validated_data)


# Serializador para el modelo Tbl_Repuesto
class RepuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbl_Repuesto  # Especifica el modelo Tbl_Repuesto para este serializador
        fields = '__all__'  # Serializa todos los campos del modelo

    # Método que devuelve tanto la estructura como los valores de la tabla programa
    def to_representation(self, instance):
        # Verificar si la solicitud es una solicitud GET
        if 'request' in self.context:
            # Si es una solicitud GET, se agregan campos adicionales a la representación
            representation = super().to_representation(instance)

            # Obtener el programa asociado a la categoría del objeto 'instance'
            # y agregar la información de la categoría serializada a la representación.
            # 'CategoriaSerializer' convierte el objeto 'Rep_categoria' en un formato adecuado
            # para la respuesta, usando el contexto de la solicitud.
            representation['Rep_categoria'] = CategoriaSerializer(
                instance.Rep_categoria, context=self.context).data

            # Devolver la representación con los campos adicionales (incluyendo la categoría)
            return representation
        # Si la solicitud no es GET, simplemente devolver la representación normal
        else:
            return super().to_representation(instance)

    def create(self, validated_data):
        """
        Similar al método 'create' de la clase CategoriaSerializer, permite crear múltiples repuestos
        o uno solo, según el tipo de datos que se pasen (lista o diccionario).
        """
        if isinstance(validated_data, list):
            # Crear una lista de instancias de Tbl_Repuesto
            repuestos = [Tbl_Repuesto(**item) for item in validated_data]
            # Guardar los repuestos de manera masiva
            return Tbl_Repuesto.objects.bulk_create(repuestos)
        # Crear un solo repuesto
        return Tbl_Repuesto.objects.create(**validated_data)

    def update(self, instance, validated_data):

        nueva_foto = validated_data.get('Rep_imagen', None)

        # 👉 Si viene una nueva foto, y ya hay una foto anterior, la borramos
        if nueva_foto and instance.Rep_imagen and instance.Rep_imagen != nueva_foto:
            instance.Rep_imagen.delete(save=False)

        # 👉 Si se quiere eliminar la foto (null), y hay una foto, también la borramos
        if 'Rep_imagen' in validated_data and validated_data['Rep_imagen'] is None:
            if instance.Rep_imagen:
                instance.Rep_imagen.delete(save=False)

        """
        Actualiza los repuestos de manera masiva si 'validated_data' es una lista, basándose en el ID de cada uno.
        """
        if isinstance(validated_data, list):
            # Mapear los programas existentes por su ID
            # Mapea los IDs a las instancias
            repuesto_mapping = {repuesto.id: repuesto for repuesto in instance}
            ret = []

            # Itera sobre los datos validados para actualizar los repuestos
            for item in validated_data:
                # Obtiene el repuesto por su ID
                repuesto = repuesto_mapping.get(item.get('id'))
                for attr, value in item.items():
                    # Actualiza los atributos del repuesto
                    setattr(repuesto, attr, value)
                repuesto.save()  # Guarda el repuesto actualizado
                # Añade el repuesto actualizado a la lista
                ret.append(repuesto)

            return ret  # Devuelve los repuestos actualizados
        # Si no es una lista, actualiza un solo repuesto
        return super().update(instance, validated_data)

# Serializador para el modelo Tbl_Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbl_Usuario  # Especifica el modelo Tbl_Usuario para este serializador
        fields = '__all__'

    def create(self, validated_data):
        """
        Crea un usuario o varios usuarios, dependiendo de si 'validated_data' es un diccionario o una lista.
        """
        if isinstance(validated_data, list):
            # Crea instancias de Tbl_Usuario
            usuarios = [Tbl_Usuario(**item) for item in validated_data]
            # Inserta todos los usuarios en la base de datos
            return Tbl_Usuario.objects.bulk_create(usuarios)
        # Crea un solo usuario
        return Tbl_Usuario.objects.create(**validated_data)

    def update(self, instance, validated_data):

        nueva_foto = validated_data.get('Usu_foto', None)

        # 👉 Si viene una nueva foto, y ya hay una foto anterior, la borramos
        if nueva_foto and instance.Usu_foto and instance.Usu_foto != nueva_foto:
            instance.Usu_foto.delete(save=False)

        # 👉 Si se quiere eliminar la foto (null), y hay una foto, también la borramos
        if 'Usu_foto' in validated_data and validated_data['Usu_foto'] is None:
            if instance.Usu_foto:
                instance.Usu_foto.delete(save=False)

        """
        Actualiza usuarios de manera masiva o individual, dependiendo de los datos recibidos.
        """
        if isinstance(validated_data, list):
            # Mapea los IDs de usuarios existentes
            usuario_mapping = {usuario.id: usuario for usuario in instance}
            ret = []

            # Itera sobre los datos para actualizar cada usuario
            for item in validated_data:
                # Obtiene el usuario por su ID
                usuario = usuario_mapping.get(item.get('id'))
                for attr, value in item.items():
                    # Actualiza los atributos del usuario
                    setattr(usuario, attr, value)
                usuario.save()  # Guarda el usuario actualizado
                ret.append(usuario)  # Añade el usuario actualizado a la lista

            return ret  # Devuelve la lista de usuarios actualizados
        # Si no es una lista, actualiza un solo usuario
        return super().update(instance, validated_data)


# Serializador para el modelo Tbl_Movimiento
class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbl_Movimiento  # Especifica el modelo Tbl_Movimiento para este serializador
        fields = '__all__'

    # Método que devuelve tanto la estructura como los valores de la tabla programa
    def to_representation(self, instance):
        # Verificar si la solicitud es una solicitud GET
        if 'request' in self.context:
            # Si es una solicitud GET, se agregan campos adicionales a la representación
            representation = super().to_representation(instance)

            # Obtener el usuario asociado al movimiento y agregar la información serializada
            # de 'Mov_usuario' a la representación. Se utiliza el serializador 'UsuarioSerializer'
            # para convertir el objeto 'Mov_usuario' a un formato adecuado para la respuesta.
            representation['Mov_usuario'] = UsuarioSerializer(
                instance.Mov_usuario, context=self.context).data

            # Obtener el repuesto asociado al movimiento y agregar la información serializada
            # de 'Mov_repuesto' a la representación. Se utiliza el serializador 'RepuestoSerializer'
            # para convertir el objeto 'Mov_repuesto' a un formato adecuado para la respuesta.
            representation['Mov_repuesto'] = RepuestoSerializer(
                instance.Mov_repuesto, context=self.context).data

            # Devolver la representación con los campos adicionales (usuario y repuesto)
            return representation
        # Si la solicitud no es GET, simplemente devolver la representación normal
        else:
            return super().to_representation(instance)

    def create(self, validated_data):
        """
        Crea uno o varios movimientos dependiendo de si 'validated_data' es una lista o un solo objeto.
        """
        if isinstance(validated_data, list):
            # Crear instancias de Tbl_Movimiento
            movimientos = [Tbl_Movimiento(**item) for item in validated_data]
            # Guardar todos los movimientos de una sola vez
            return Tbl_Movimiento.objects.bulk_create(movimientos)
        # Crear un solo movimiento
        return Tbl_Movimiento.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza varios movimientos de manera masiva si se reciben en formato de lista.
        """
        if isinstance(validated_data, list):
            movimiento_mapping = {
                movimiento.id: movimiento for movimiento in instance}  # Mapea los IDs
            ret = []

            # Itera sobre cada movimiento a actualizar
            for item in validated_data:
                movimiento = movimiento_mapping.get(
                    item.get('id'))  # Obtiene el movimiento por ID
                for attr, value in item.items():
                    # Actualiza los atributos del movimiento
                    setattr(movimiento, attr, value)
                movimiento.save()  # Guarda el movimiento actualizado
                # Añade el movimiento actualizado a la lista
                ret.append(movimiento)

            # Devolver la lista de programas actualizados
            return ret
        # Actualizar un solo programa
        return super().update(instance, validated_data)


class HerramientaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbl_Herramienta
        fields = '__all__'

    # Método que devuelve tanto la estructura como los valores de la tabla programa
    def to_representation(self, instance):
        # Verificar si la solicitud es una solicitud GET
        if 'request' in self.context:
            # Si es una solicitud GET, se agregan campos adicionales a la representación
            representation = super().to_representation(instance)

            # Obtener la categoría asociada al programa y agregar la información serializada
            # de 'Her_categoria' a la representación. Se utiliza el serializador 'CategoriaSerializer'
            # para convertir el objeto 'Her_categoria' a un formato adecuado para la respuesta.
            representation['Her_categoria'] = CategoriaSerializer(
                instance.Her_categoria, context=self.context).data

            # Devolver la representación con los campos adicionales (categoría)
            return representation
        # Si la solicitud no es GET, simplemente devolver la representación normal
        else:
            return super().to_representation(instance)

    # Función para crear programas de manera masiva

    def create(self, validated_data):
        # Verificar si los datos son una lista
        if isinstance(validated_data, list):
            # Crear una instancia de Programa para cada elemento de la lista
            herramientas = [Tbl_Herramienta(**item) for item in validated_data]
            # Guardar los programas en la base de datos
            return Tbl_Herramienta.objects.bulk_create(herramientas)
        # Crear un solo programa
        return Tbl_Herramienta.objects.create(**validated_data)

    # Función para actualizar programas de manera masiva
    def update(self, instance, validated_data):

        nueva_foto = validated_data.get('Her_imagen', None)

        # 👉 Si viene una nueva foto, y ya hay una foto anterior, la borramos
        if nueva_foto and instance.Her_imagen and instance.Her_imagen != nueva_foto:
            instance.Her_imagen.delete(save=False)

        # 👉 Si se quiere eliminar la foto (null), y hay una foto, también la borramos
        if 'Her_imagen' in validated_data and validated_data['Her_imagen'] is None:
            if instance.Her_imagen:
                instance.Her_imagen.delete(save=False)

        # Verificar si los datos son una lista
        if isinstance(validated_data, list):
            # Mapear los programas existentes por su ID
            herramienta_mapping = {
                herramienta.id: herramienta for herramienta in instance}
            # Variable para almacenar los programas actualizados
            ret = []

            # For para actualizar cada programa
            for item in validated_data:
                # Obtener el programa correspondiente al ID
                herramienta = herramienta_mapping.get(item.get('id'))
                # Actualizar los atributos del programa
                for attr, value in item.items():
                    setattr(herramienta, attr, value)
                # Guardar el programa
                herramienta.save()
                # Agregar el programa actualizado a la lista
                ret.append(herramienta)

            # Devolver la lista de programas actualizados
            return ret
        # Actualizar un solo programa
        return super().update(instance, validated_data)


class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbl_Prestamo
        fields = '__all__'

    # Método que devuelve tanto la estructura como los valores de la tabla programa
    def to_representation(self, instance):
        # Verificar si la solicitud es una solicitud GET
        if 'request' in self.context:
            # Si es una solicitud GET, se agregan campos adicionales a la representación
            representation = super().to_representation(instance)

            # Obtener la herramienta asociada al programa y agregar la información serializada
            # de 'Pre_herramienta' a la representación. Se utiliza el serializador 'HerramientaSerializer'
            # para convertir el objeto 'Pre_herramienta' a un formato adecuado para la respuesta.
            representation['Pre_herramienta'] = HerramientaSerializer(
                instance.Pre_herramienta, context=self.context).data

            # Devolver la representación con los campos adicionales (herramienta)
            return representation
        # Si la solicitud no es GET, simplemente devolver la representación normal
        else:
            return super().to_representation(instance)

    # Función para crear programas de manera masiva

    def create(self, validated_data):
        # Verificar si los datos son una lista
        if isinstance(validated_data, list):
            # Crear una instancia de Programa para cada elemento de la lista
            prestamos = [Tbl_Prestamo(**item) for item in validated_data]
            # Guardar los programas en la base de datos
            return Tbl_Prestamo.objects.bulk_create(prestamos)
        # Crear un solo programa
        return Tbl_Prestamo.objects.create(**validated_data)

    # Función para actualizar programas de manera masiva
    def update(self, instance, validated_data):
        # Verificar si los datos son una lista
        if isinstance(validated_data, list):
            # Mapear los programas existentes por su ID
            prestamo_mapping = {prestamo.id: prestamo for prestamo in instance}
            # Variable para almacenar los programas actualizados
            ret = []

            # For para actualizar cada programa
            for item in validated_data:
                # Obtener el programa correspondiente al ID
                prestamo = prestamo_mapping.get(item.get('id'))
                # Actualizar los atributos del programa
                for attr, value in item.items():
                    setattr(prestamo, attr, value)
                # Guardar el programa
                prestamo.save()
                # Agregar el programa actualizado a la lista
                ret.append(prestamo)

            return ret  # Devuelve la lista de movimientos actualizados
        # Si no es una lista, actualiza un solo movimiento
        return super().update(instance, validated_data)

# Serializador para el modelo Tbl_Mensaje


class MensajeSerializer(serializers.ModelSerializer):
    # Clase Meta para definir el modelo y los campos a serializar
    class Meta:
        # Especifica el modelo Tbl_Mensaje que será utilizado en este serializador
        model = Tbl_Mensaje
        fields = '__all__'  # Serializa todos los campos del modelo sin excepción

    # Función para crear registros de mensajes de manera masiva
    def create(self, validated_data):
        """
        Este método permite crear uno o varios registros del modelo Tbl_Mensaje de manera masiva.
        Si se recibe una lista de datos en 'validated_data', se crean todos los mensajes de una sola vez.
        Si se recibe un solo diccionario, se crea un solo mensaje.
        """
        # Verificar si los datos validados son una lista
        if isinstance(validated_data, list):
            # Crear una instancia de Tbl_Mensaje para cada elemento de la lista de datos
            mensajes = [Tbl_Mensaje(**item) for item in validated_data]
            # Guardar todos los mensajes en la base de datos de una sola vez utilizando bulk_create()
            return Tbl_Mensaje.objects.bulk_create(mensajes)
        # Si no es una lista, crear un solo mensaje
        return Tbl_Mensaje.objects.create(**validated_data)

    # Función para actualizar registros de mensajes de manera masiva
    def update(self, instance, validated_data):
        """
        Este método permite actualizar los registros existentes del modelo Tbl_Mensaje. Si se recibe
        una lista de mensajes en 'validated_data', se actualizan múltiples mensajes en la base de datos
        basándose en el ID de cada uno. Si es un solo mensaje, se actualiza uno solo.
        """
        # Verificar si los datos validados son una lista
        if isinstance(validated_data, list):
            # Crear un diccionario para mapear los IDs de los mensajes existentes a sus instancias en la base de datos
            mensaje_mapping = {mensaje.id: mensaje for mensaje in instance}
            # Lista para almacenar los mensajes actualizados
            ret = []

            # Iterar sobre cada mensaje de la lista de datos validados
            for item in validated_data:
                # Obtener el mensaje correspondiente por su ID
                mensaje = mensaje_mapping.get(item.get('id'))
                for attr, value in item.items():
                    # Actualizar el atributo con el nuevo valor
                    setattr(mensaje, attr, value)
                mensaje.save()  # Guardar los cambios realizados en el mensaje
                # Agregar el mensaje actualizado a la lista de resultados
                ret.append(mensaje)

            # Devolver la lista de mensajes actualizados
            return ret
        # Si no es una lista, actualizar solo un registro utilizando el método `super().update`
        return super().update(instance, validated_data)
