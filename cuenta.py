from transaccion import Transaccion

class CuentaFamiliar:
    def __init__(self):
        self.__saldo = 0.0
        self.__historial = []

    def obtener_saldo(self):
        return self.__saldo

    def registrar_ingreso(self, nombre_hijo, monto):
        self.__saldo += monto
        # Se crea la transacción y se llama a su nuevo metodo interactivo
        nueva_tx = Transaccion(nombre_hijo, "Ingreso", monto)
        nueva_tx.solicitar_concepto()

        self.__historial.append(nueva_tx)
        return f"Depósito exitoso. Nuevo saldo: ${self.__saldo}"

    def realizar_retiro(self, nombre_padre, monto):
        if monto > self.__saldo:
            raise ValueError(f"Fondos insuficientes. Saldo actual: ${self.__saldo}")
            #---------->  raise   <-------------
        self.__saldo -= monto
        # Se crea la transacción y se llama a su nuevo metodo interactivo
        nueva_tx = Transaccion(nombre_padre, "Retiro", monto)
        nueva_tx.solicitar_concepto()

        self.__historial.append(nueva_tx)
        return f"Retiro autorizado. Nuevo saldo: ${self.__saldo}"

    # NUEVO: La cuenta maneja el menú, limpiando el main.py
    def ejecutar_menu(self, padre, hijos):
        print("\n\t MENÚ PRINCIPAL ")
        print("1. Registrar depósito (Hijos)")
        print("2. Registrar retiro (Padres)")
        print("3. Ver saldo e historial")
        print("4. Salir")
        opcion = input("Elige una opción segun el número = (1 a 4): ")

        if opcion == "1":
            id_hijo = input("\nSeleccione hijo (1. Kevin )( 2. Laura): ")
            if id_hijo in hijos:
                # Llamada polimórfica interactiva
                print(hijos[id_hijo].operar_interactivo(self))
            else:
                print("Hijo no válido.")
        elif opcion == "2":
            # Llamada polimórfica interactiva
            print(padre.operar_interactivo(self))
        elif opcion == "3":
            self.mostrar_estado()
        elif opcion == "4":
            print("Saliendo del sistema...")
            return False  # Indica al main que rompa el ciclo
        else:
            print("Opción inválida.")

        return True  # Indica al main que el ciclo continúa

    def mostrar_estado(self):
        print(f"\n\t ESTADO DE LA CUENTA ")
        print(f"Saldo Total: ${self.__saldo}")
        if not self.__historial:
            print("Sin movimientos.")
        else:
            for tx in self.__historial:
                print(tx.mostrar_detalle())