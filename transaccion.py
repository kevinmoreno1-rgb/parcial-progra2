class Transaccion:
    def __init__(self, id_transaccion, monto, fecha, concepto):
        self.__id_transaccion = id_transaccion
        self.__monto = monto
        self.__fecha = fecha
        self.__concepto = concepto

    def es_monto_valido(self):
        return self.__monto > 0

    def modificar_concepto(self, nuevo_concepto):
        if len(nuevo_concepto.strip()) > 0:
            self.__concepto = nuevo_concepto.strip()

    def aplicar_a_saldo(self, saldo_actual, es_ingreso=True):
        if es_ingreso:
            return saldo_actual + self.__monto
        return saldo_actual - self.__monto

    def obtener_resumen(self):
        return f"ID: {self.__id_transaccion} | Fecha: {self.__fecha} | Monto: ${self.__monto:,.2f} | Concepto: {self.__concepto}"