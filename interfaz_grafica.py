import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from deposito import Deposito
from egreso import Egreso

class InterfazGrafica:
    def __init__(self, cuenta, usuarios, backend, notificacion, meta, reporte):
        self.__cuenta = cuenta
        self.__usuarios = usuarios
        self.__backend = backend
        self.__notificacion = notificacion
        self.__meta = meta
        self.__reporte = reporte

        self.__ventana = tk.Tk()
        self.__ventana.title("FamiCuenta - Monitoreo Familiar")
        self.__ventana.geometry("820x560")

        self.__tipo_var = tk.StringVar(value="INGRESO")
        self.__usuario_var = tk.StringVar(value=list(self.__usuarios.keys())[0])

        self.__crear_menu()
        self.__crear_widgets()
        self.__cargar_tabla()

    def __crear_menu(self):
        barra_menu = tk.Menu(self.__ventana)
        menu_opciones = tk.Menu(barra_menu, tearoff=0)
        menu_opciones.add_command(label="Configurar Meta de Ahorro", command=self.__abrir_ventana_meta)
        menu_opciones.add_command(label="Exportar Reporte (.txt)", command=self.__exportar_reporte)
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Salir", command=self.__ventana.quit)
        barra_menu.add_cascade(label="Opciones", menu=menu_opciones)
        self.__ventana.config(menu=barra_menu)

    def __crear_widgets(self):
        # Frame 1: Estado de cuenta y Meta (Elemento adicional: ttk.Progressbar)
        frame_estado = tk.Frame(self.__ventana, pady=8, padx=10)
        frame_estado.pack(fill="x")

        self.__lbl_estado = tk.Label(frame_estado, text=self.__cuenta.consultar_estado(), font=("Arial", 11, "bold"))
        self.__lbl_estado.pack(anchor="w")

        self.__lbl_meta = tk.Label(frame_estado, text=self.__meta.obtener_descripcion())
        self.__lbl_meta.pack(anchor="w")

        self.__barra_progreso = ttk.Progressbar(frame_estado, length=400, mode="determinate")
        self.__barra_progreso.pack(anchor="w", pady=3)

        # Frame 2: Formulario sencillo
        frame_form = tk.LabelFrame(self.__ventana, text="Registrar / Editar Movimiento", padx=10, pady=8)
        frame_form.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_form, text="Usuario:").grid(row=0, column=0, sticky="w")
        combo_usr = ttk.Combobox(frame_form, textvariable=self.__usuario_var, values=list(self.__usuarios.keys()), state="readonly", width=15)
        combo_usr.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_form, text="PIN:").grid(row=0, column=2, sticky="w")
        self.__entry_pin = tk.Entry(frame_form, show="*", width=12)
        self.__entry_pin.grid(row=0, column=3, padx=5, pady=2)

        tk.Radiobutton(frame_form, text="Ingreso (Abono)", variable=self.__tipo_var, value="INGRESO").grid(row=0, column=4, padx=5)
        tk.Radiobutton(frame_form, text="Egreso (Retiro/Pago)", variable=self.__tipo_var, value="EGRESO").grid(row=0, column=5, padx=5)

        tk.Label(frame_form, text="Monto:").grid(row=1, column=0, sticky="w")
        self.__entry_monto = tk.Entry(frame_form, width=18)
        self.__entry_monto.grid(row=1, column=1, padx=5, pady=4)

        tk.Label(frame_form, text="Concepto:").grid(row=1, column=2, sticky="w")
        self.__entry_concepto = tk.Entry(frame_form, width=22)
        self.__entry_concepto.grid(row=1, column=3, padx=5, pady=4)

        tk.Label(frame_form, text="Emisor / Destino:").grid(row=1, column=4, sticky="w")
        self.__entry_detalle = tk.Entry(frame_form, width=20)
        self.__entry_detalle.grid(row=1, column=5, padx=5, pady=4)

        # Botones de acción
        frame_botones = tk.Frame(frame_form)
        frame_botones.grid(row=2, column=0, columnspan=6, pady=6)

        tk.Button(frame_botones, text="Registrar Movimiento", command=self.__registrar).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Actualizar Concepto Seleccionado", command=self.__actualizar).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Eliminar Seleccionado", command=self.__eliminar).pack(side="left", padx=5)

        # Frame 3: Tabla Treeview
        frame_tabla = tk.Frame(self.__ventana, padx=10, pady=5)
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("ID", "Tipo", "Monto", "Fecha", "Concepto", "Detalle", "Usuario")
        self.__tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=11)
        for col in columnas:
            self.__tabla.heading(col, text=col)
            self.__tabla.column(col, width=110)
        self.__tabla.pack(fill="both", expand=True)

        # Uso de .bind(): doble clic en una fila carga su concepto en el Entry
        self.__tabla.bind("<Double-1>", self.__seleccionar_fila)

    def __cargar_tabla(self):
        for item in self.__tabla.get_children():
            self.__tabla.delete(item)
        filas = self.__backend.leer_movimientos()
        for fila in filas:
            self.__tabla.insert("", "end", values=fila)

        # Actualizar estado y barra de progreso
        self.__lbl_estado.config(text=self.__cuenta.consultar_estado())
        saldo_texto = self.__cuenta.consultar_estado().split("$")[1].replace(",", "")
        self.__meta.actualizar_progreso(float(saldo_texto))
        self.__lbl_meta.config(text=self.__meta.obtener_descripcion())
        self.__barra_progreso["value"] = self.__meta.calcular_porcentaje()

    def __seleccionar_fila(self, event):
        seleccion = self.__tabla.selection()
        if seleccion:
            valores = self.__tabla.item(seleccion[0], "values")
            self.__entry_concepto.delete(0, tk.END)
            self.__entry_concepto.insert(0, valores[4])

    def __registrar(self):
        try:
            nombre_usr = self.__usuario_var.get()
            usuario_obj = self.__usuarios[nombre_usr]
            pin = self.__entry_pin.get().strip()

            if not usuario_obj.validar_pin(pin):
                raise PermissionError("PIN incorrecto para el usuario seleccionado.")

            monto = float(self.__entry_monto.get())
            concepto = self.__entry_concepto.get().strip()
            detalle = self.__entry_detalle.get().strip() or nombre_usr
            if not concepto:
                raise ValueError("Debe escribir un concepto.")

            tipo = self.__tipo_var.get()
            id_tx = f"TX-{len(self.__backend.leer_movimientos()) + 101}"
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

            if tipo == "INGRESO":
                dep = Deposito(id_tx, monto, fecha, concepto, detalle)
                self.__cuenta.registrar_ingreso(dep)
            else:
                egr = Egreso(id_tx, monto, fecha, concepto, detalle, "General")
                self.__cuenta.procesar_retiro_o_pago(egr, usuario_obj)

            self.__backend.guardar_movimiento(id_tx, tipo, monto, fecha, concepto, detalle, nombre_usr)
            aviso = self.__notificacion.generar_aviso(tipo, monto, concepto, nombre_usr)
            self.__cargar_tabla()
            messagebox.showinfo("Éxito", aviso)

        except (ValueError, PermissionError) as err:
            messagebox.showerror("Error de validación", str(err))
        except Exception as err:
            messagebox.showerror("Error", f"Ocurrió un error: {err}")

    def __actualizar(self):
        try:
            seleccion = self.__tabla.selection()
            if not seleccion:
                raise ValueError("Seleccione un movimiento de la tabla primero.")
            id_tx = self.__tabla.item(seleccion[0], "values")[0]
            nuevo_concepto = self.__entry_concepto.get()
            self.__backend.actualizar_concepto(id_tx, nuevo_concepto)
            self.__cargar_tabla()
            messagebox.showinfo("Actualizado", "Concepto actualizado en Excel.")
        except Exception as err:
            messagebox.showerror("Error", str(err))

    def __eliminar(self):
        try:
            seleccion = self.__tabla.selection()
            if not seleccion:
                raise ValueError("Seleccione un movimiento de la tabla para eliminar.")
            id_tx = self.__tabla.item(seleccion[0], "values")[0]
            if messagebox.askyesno("Confirmar", f"¿Eliminar el registro {id_tx} de Excel?"):
                self.__backend.eliminar_movimiento(id_tx)
                self.__cargar_tabla()
        except Exception as err:
            messagebox.showerror("Error", str(err))

    def __abrir_ventana_meta(self):
        ventana_sec = tk.Toplevel(self.__ventana)
        ventana_sec.title("Meta de Ahorro")
        ventana_sec.geometry("300x160")

        tk.Label(ventana_sec, text="Nombre de la meta:").pack(pady=3)
        entry_nom = tk.Entry(ventana_sec)
        entry_nom.pack()

        tk.Label(ventana_sec, text="Monto objetivo ($):").pack(pady=3)
        entry_obj = tk.Entry(ventana_sec)
        entry_obj.pack()

        def guardar_meta():
            try:
                self.__meta.configurar_meta(entry_nom.get() or "Ahorro Hogar", float(entry_obj.get()))
                self.__cargar_tabla()
                ventana_sec.destroy()
            except Exception as err:
                messagebox.showerror("Error", str(err), parent=ventana_sec)

        tk.Button(ventana_sec, text="Guardar Meta", command=guardar_meta).pack(pady=10)

    def __exportar_reporte(self):
        try:
            ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")])
            if ruta:
                self.__reporte.exportar_txt(ruta, self.__cuenta.consultar_estado(), self.__backend.leer_movimientos())
                messagebox.showinfo("Exportado", "Reporte guardado correctamente.")
        except Exception as err:
            messagebox.showerror("Error", str(err))

    def iniciar(self):
        self.__ventana.mainloop()