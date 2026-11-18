class Cuenta:
    def __init__(self, numero_cuenta, saldo_inicial):
        self._numero_cuenta = numero_cuenta
        self._saldo = saldo_inicial  # Un guion bajo para que la clase hija pueda usarlo

    def consultar_estado(self):
        return f"Cuenta N°: {self._numero_cuenta} | Saldo: ${self._saldo:,.2f}"