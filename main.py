from padre import Padre
from hijo import Hijo
from cuenta_familiar import CuentaFamiliar
from gestor_excel import GestorExcel
from notificacion import Notificacion
from meta_ahorro import MetaAhorro
from reporte_familiar import ReporteFamiliar
from interfaz_grafica import InterfazGrafica

# 1. Creación de los objetos principales (Ahora usando las clases Padre e Hijo)
usuarios_familia = {
    "Mamá": Padre("U01", "Mamá", "1234"),
    "Papá": Padre("U02", "Papá", "1234"),
    "Carlos": Hijo("U03", "Carlos", "0000"),
    "Sofía": Hijo("U04", "Sofía", "0000"),
    "Andrés": Hijo("U05", "Andrés", "0000")
}

cuenta_bancaria = CuentaFamiliar("245-89100-12", 0.0, list(usuarios_familia.values()))

# 2. Creación de objetos auxiliares
backend_excel = GestorExcel("famicuenta.xlsx")
sistema_notificacion = Notificacion("FamiCuenta")
meta = MetaAhorro("Fondo de Emergencia", 1000000.0)
reporte = ReporteFamiliar("Historial de la Familia")

# 3. Iniciar ejecución general de la aplicación
app = InterfazGrafica(cuenta_bancaria, usuarios_familia, backend_excel, sistema_notificacion, meta, reporte)
app.iniciar()