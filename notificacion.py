class Notificacion:
    def __init__(self, sistema):
        self.__sistema = sistema

    def generar_aviso(self, tipo, monto, concepto, usuario):
        return f"[{self.__sistema}] {tipo} exitoso de ${monto:,.2f} ({concepto}) - Usuario: {usuario}"