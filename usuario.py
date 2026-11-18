class Usuario:
    def __init__(self, id_usuario, nombre):
        self.__id_usuario = id_usuario
        self.__nombre = nombre

    def obtener_nombre(self):
        return self.__nombre

    def obtener_id(self):
        return self.__id_usuario

    def realizar_operacion(self, cuenta, monto, concepto=""):
        pass

    # Nuevo metodo base para pedir datos interactivos (Polimorfismo)
    def operar_interactivo(self, cuenta):
        pass