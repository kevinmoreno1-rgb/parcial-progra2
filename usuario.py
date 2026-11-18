class Usuario:
    def __init__(self, id_usuario, nombre, rol, pin_seguridad):
        self.__id_usuario = id_usuario
        self.__nombre = nombre
        self.__rol = rol
        self.__pin_seguridad = pin_seguridad

    def validar_pin(self, pin_ingresado):
        return self.__pin_seguridad == pin_ingresado

    def es_padre(self):
        return self.__rol.strip().upper() == "PADRE"

    def coincide_nombre(self, nombre_buscado):
        return self.__nombre.strip().lower() == nombre_buscado.strip().lower()

    def mostrar_identificacion(self):
        return f"{self.__nombre} (Rol: {self.__rol})"