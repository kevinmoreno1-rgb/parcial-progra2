from usuario import Usuario

class Padre(Usuario):
    def __init__(self, id_usuario, nombre):
        super().__init__(id_usuario, nombre)

    def realizar_operacion(self, cuenta, monto):
        return cuenta.realizar_retiro(self.obtener_nombre(), monto)

    def operar_interactivo(self, cuenta):
        print(f"\n\t Retiro de {self.obtener_nombre()} ")
        monto = float(input("Ingresa el monto a retirar: $"))
        return self.realizar_operacion(cuenta, monto)