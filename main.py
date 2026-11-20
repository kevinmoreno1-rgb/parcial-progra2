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
    "Kevin": Hijo("U03", "Kevin", "0000"),
    "Laura": Hijo("U04", "Laura", "0000"),
    "Jasson": Hijo("U05", "Jasson", "0000")
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