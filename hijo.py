from usuario import Usuario

class Hijo(Usuario):
    def __init__(self, id_usuario, nombre):
        super().__init__(id_usuario, nombre)

    def realizar_operacion(self, cuenta, monto):
        if monto <= 0:
            # LANZAMIENTO DE EXCEPCIÓN: si el monto es negativo o cero
            raise ValueError(f"El monto debe ser mayor a 0.")
        return cuenta.registrar_ingreso(self.obtener_nombre(), monto)

    # El hijo pide el dinero, pero ya no pide el concepto (eso lo hace transaccion.py)
    def operar_interactivo(self, cuenta):
        print(f"\n\t Depósito de {self.obtener_nombre()} ")
        monto = float(input("Ingresa el monto a depositar: $"))
        return self.realizar_operacion(cuenta, monto)