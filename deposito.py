from transaccion import Transaccion

class Deposito(Transaccion):
    def __init__(self, id_transaccion, monto, fecha, concepto, hermano_emisor):
        super().__init__(id_transaccion, monto, fecha, concepto)
        self.__hermano_emisor = hermano_emisor

    def es_emisor(self, nombre_hermano):
        return self.__hermano_emisor.strip().lower() == nombre_hermano.strip().lower()

    def obtener_resumen(self):
        resumen_base = super().obtener_resumen()
        return f"[INGRESO] {resumen_base} | Realizado por: {self.__hermano_emisor}"