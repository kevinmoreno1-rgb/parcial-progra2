class ReporteFamiliar:
    def __init__(self, titulo):
        self.__titulo = titulo

    def exportar_txt(self, ruta_archivo, estado_cuenta, filas_excel):
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(f"=== {self.__titulo} ===\n")
            archivo.write(f"{estado_cuenta}\n")
            archivo.write("-" * 60 + "\n")
            for fila in filas_excel:
                archivo.write(f"{fila[0]} | {fila[1]} | ${fila[2]:,.2f} | {fila[3]} | {fila[4]} | {fila[5]} | {fila[6]}\n")