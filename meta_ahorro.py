class MetaAhorro:
    def __init__(self, nombre_meta, monto_objetivo):
        self.__nombre_meta = nombre_meta
        self.__monto_objetivo = monto_objetivo
        self.__monto_actual = 0.0

    def configurar_meta(self, nuevo_nombre, nuevo_objetivo):
        if nuevo_objetivo <= 0:
            raise ValueError("El objetivo de la meta debe ser mayor a cero.")
        self.__nombre_meta = nuevo_nombre
        self.__monto_objetivo = nuevo_objetivo

    def actualizar_progreso(self, monto_actual):
        self.__monto_actual = max(0.0, monto_actual)

    def calcular_porcentaje(self):
        if self.__monto_objetivo <= 0:
            return 0
        porcentaje = (self.__monto_actual / self.__monto_objetivo) * 100
        return min(100.0, porcentaje)

    def obtener_descripcion(self):
        return f"Meta ({self.__nombre_meta}): ${self.__monto_actual:,.0f} / ${self.__monto_objetivo:,.0f} ({self.calcular_porcentaje():.1f}%)"