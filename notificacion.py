class Notificacion:
    def __init__(self, sistema):
        self.__sistema = sistema
        self.__ultimo_mensaje = "Sin movimientos recientes."

    def generar_aviso(self, tipo, monto, concepto, usuario):
        self.__ultimo_mensaje = f"[{self.__sistema}] {tipo} de ${monto:,.2f} ({concepto}) - Por: {usuario}"
        return self.__ultimo_mensaje

    def obtener_ultimo_aviso(self):
        return self.__ultimo_mensaje