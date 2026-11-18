import os
import openpyxl
from deposito import Deposito
from egreso import Egreso

class GestorExcel:
    def __init__(self, nombre_archivo="famicuenta.xlsx"):
        self.__nombre_archivo = nombre_archivo
        self.inicializar_archivo()

    def inicializar_archivo(self):
        if not os.path.exists(self.__nombre_archivo):
            libro = openpyxl.Workbook()
            hoja = libro.active
            hoja.title = "Movimientos"
            hoja.append(["ID", "Tipo", "Monto", "Fecha", "Concepto", "Detalle", "Usuario"])
            libro.save(self.__nombre_archivo)

    def guardar_movimiento(self, id_tx, tipo, monto, fecha, concepto, detalle, usuario):
        libro = openpyxl.load_workbook(self.__nombre_archivo)
        hoja = libro["Movimientos"]
        hoja.append([id_tx, tipo, float(monto), fecha, concepto, detalle, usuario])
        libro.save(self.__nombre_archivo)

    def leer_movimientos(self):
        libro = openpyxl.load_workbook(self.__nombre_archivo)
        hoja = libro["Movimientos"]
        registros = []
        for fila in hoja.iter_rows(min_row=2, values_only=True):
            if fila[0] is not None:
                registros.append(list(fila))
        return registros

    def actualizar_concepto(self, id_tx, nuevo_concepto):
        if not nuevo_concepto.strip():
            raise ValueError("El nuevo concepto no puede estar vacío.")
        libro = openpyxl.load_workbook(self.__nombre_archivo)
        hoja = libro["Movimientos"]
        encontrado = False
        for fila in hoja.iter_rows(min_row=2):
            if str(fila[0].value) == str(id_tx):
                fila[4].value = nuevo_concepto.strip()
                encontrado = True
                break
        if not encontrado:
            raise ValueError("No se encontró el registro en Excel.")
        libro.save(self.__nombre_archivo)

    def eliminar_movimiento(self, id_tx):
        libro = openpyxl.load_workbook(self.__nombre_archivo)
        hoja = libro["Movimientos"]
        fila_borrar = None
        for idx, fila in enumerate(hoja.iter_rows(min_row=2), start=2):
            if str(fila[0].value) == str(id_tx):
                fila_borrar = idx
                break
        if fila_borrar is None:
            raise ValueError("No se encontró el registro para eliminar.")
        hoja.delete_rows(fila_borrar)
        libro.save(self.__nombre_archivo)

    def sincronizar_cuenta(self, cuenta, usuario_padre):
        for fila in self.leer_movimientos():
            id_tx, tipo, monto, fecha, concepto, detalle, _ = fila
            if tipo == "INGRESO":
                dep = Deposito(id_tx, float(monto), fecha, concepto, detalle)
                cuenta.registrar_ingreso(dep)
            elif tipo == "EGRESO":
                egr = Egreso(id_tx, float(monto), fecha, concepto, detalle, "General")
                cuenta.procesar_retiro_o_pago(egr, usuario_padre)