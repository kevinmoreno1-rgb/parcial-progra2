import os
import openpyxl

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
        libro = openpyxl.load_workbook(self.__nombre_archivo)
        hoja = libro["Movimientos"]
        for fila in hoja.iter_rows(min_row=2):
            if str(fila[0].value) == str(id_tx):
                fila[4].value = nuevo_concepto.strip()
                break
        libro.save(self.__nombre_archivo)

    def eliminar_movimiento(self, id_tx):
        libro = openpyxl.load_workbook(self.__nombre_archivo)
        hoja = libro["Movimientos"]
        fila_borrar = None
        for idx, fila in enumerate(hoja.iter_rows(min_row=2), start=2):
            if str(fila[0].value) == str(id_tx):
                fila_borrar = idx
                break
        if fila_borrar is not None:
            hoja.delete_rows(fila_borrar)
            libro.save(self.__nombre_archivo)