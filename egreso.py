from transaccion import Transaccion

class Egreso(Transaccion):
    def __init__(self, id_transaccion, monto, fecha, concepto, destino_pago, categoria):
        super().__init__(id_transaccion, monto, fecha, concepto)
        self.__destino_pago = destino_pago
        self.__categoria = categoria

    def pertenece_a_categoria(self, categoria_buscada):
        return self.__categoria.strip().lower() == categoria_buscada.strip().lower()

    def obtener_resumen(self):
        resumen_base = super().obtener_resumen()
        return f"[EGRESO] {resumen_base} | Destino: {self.__destino_pago} | Categoría: {self.__categoria}"