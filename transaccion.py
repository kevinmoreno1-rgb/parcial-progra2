from datetime import datetime


class Transaccion:
    def __init__(self, autor, tipo, monto):
        self.__autor = autor
        self.__tipo = tipo
        self.__monto = monto
        self.__fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__concepto = ""  # Se inicializa vacío para pedirlo luego

    # NUEVO: La transacción es responsable de pedir sus propios detalles
    def solicitar_concepto(self):
        print(f"   -> Detallando la transacción de {self.__tipo}...")
        self.__concepto = input("   Escribe el concepto o motivo: ")

        # Validación: si el usuario lo deja vacío, pone un texto por defecto
        if not self.__concepto.strip():
            self.__concepto = "Sin especificar"

    def mostrar_detalle(self):
        return f"[{self.__fecha}] {self.__tipo}: ${self.__monto} | Por: {self.__autor} | Motivo: {self.__concepto}"