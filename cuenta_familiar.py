from cuenta import Cuenta


class CuentaFamiliar(Cuenta):
    def __init__(self, numero_cuenta, saldo_inicial, titulares):
        super().__init__(numero_cuenta, saldo_inicial)
        self.__titulares = titulares
        self.__historial = []

    def registrar_ingreso(self, deposito):
        if not deposito.es_monto_valido():
            raise ValueError("El monto del depósito debe ser mayor a cero.")
        self._saldo = deposito.aplicar_a_saldo(self._saldo, es_ingreso=True)
        self.__historial.append(deposito)

    def procesar_retiro_o_pago(self, egreso, usuario_actual):
        if not usuario_actual.es_padre():
            raise PermissionError("Acceso denegado: Solo nuestros padres pueden autorizar pagos.")
        if not egreso.es_monto_valido():
            raise ValueError("El monto debe ser mayor a cero.")

        nuevo_saldo = egreso.aplicar_a_saldo(self._saldo, es_ingreso=False)
        if nuevo_saldo < 0:
            raise ValueError("Saldo insuficiente en la cuenta.")

        self._saldo = nuevo_saldo
        self.__historial.append(egreso)