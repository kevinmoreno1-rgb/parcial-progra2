from cuenta import CuentaFamiliar
from hijo import Hijo
from padre import Padre


def main():
    # 1. Creación de objetos y colecciones principales
    cuenta = CuentaFamiliar()
    papa = Padre(1, "Alberto / Martha (Papás)")
    hijos = {"1": Hijo(101, "Kevin"), "2": Hijo(102, "Laura")}

    print("\t SISTEMA FAMICUENTA INICIADO ")

    # 2. Ejecución general y llamadas a los métodos
    while True:
        try:
            # Delega TODA la lógica visual a la cuenta
            continuar_sistema = cuenta.ejecutar_menu(papa, hijos)

            # Si ejecutar_menu devuelve False (opción 4), se rompe el ciclo
            if not continuar_sistema:
                break

        # 3. Manejo de excepciones centralizado
        except ValueError as e:
            print(f"\n[ALERTA DE SEGURIDAD]: {e}")
        except Exception as e:
            print(f"\n[ERROR INESPERADO]: Entrada no válida. ({e})")

if __name__ == "__main__":
    main()