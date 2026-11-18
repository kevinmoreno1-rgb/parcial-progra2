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

        self.__sincronizar_desde_excel()

        self.__ventana = tk.Tk()
        self.__ventana.title("FamiCuenta - Monitoreo Familiar")
        self.__ventana.geometry("860x560")

        self.__tipo_var = tk.StringVar(value="INGRESO")
        self.__usuario_var = tk.StringVar(value=list(self.__usuarios.keys())[0])

        self.__crear_menu()
        self.__crear_widgets()
        self.__cargar_tabla()

    def __sincronizar_desde_excel(self):
        for fila in self.__backend.leer_movimientos():
            id_tx, tipo, monto, fecha, concepto, detalle, _ = fila
            if tipo == "INGRESO":
                dep = Deposito(id_tx, float(monto), fecha, concepto, detalle)
                self.__cuenta.registrar_ingreso(dep)
            else:
                egr = Egreso(id_tx, float(monto), fecha, concepto, detalle, "General")
                self.__cuenta.procesar_retiro_o_pago(egr, self.__usuarios["Mamá"])

    def __crear_menu(self):
        barra = tk.Menu(self.__ventana)
        opciones = tk.Menu(barra, tearoff=0)
        opciones.add_command(label="Configurar Meta de Ahorro", command=self.__abrir_ventana_meta)
        opciones.add_command(label="Exportar Reporte (.txt)", command=self.__exportar_reporte)
        opciones.add_separator()
        opciones.add_command(label="Salir", command=self.__ventana.quit)
        barra.add_cascade(label="Opciones", menu=opciones)
        self.__ventana.config(menu=barra)

    def __crear_widgets(self):
        frame_estado = tk.Frame(self.__ventana, pady=10, padx=10)
        frame_estado.pack(fill="x")
        self.__lbl_estado = tk.Label(frame_estado, text="", font=("Arial", 11, "bold"))
        self.__lbl_estado.pack(anchor="w")
        self.__lbl_meta = tk.Label(frame_estado, text="")
        self.__lbl_meta.pack(anchor="w")
        #NUEVO NO VISTO EN CLASE : BARRA DE PROGRESO    NUEVO NO VISTO EN CLASE : BARRA DE PROGRESO     NUEVO NO VISTO EN CLASE : BARRA DE PROGRESO
        self.__barra_progreso = ttk.Progressbar(frame_estado, length=400, mode="determinate")
        self.__barra_progreso.pack(anchor="w", pady=3)

        frame_form = tk.LabelFrame(self.__ventana, text="Nuevo Movimiento", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_form, text="Usuario:").grid(row=0, column=0)
        ttk.Combobox(frame_form, textvariable=self.__usuario_var, values=list(self.__usuarios.keys()), state="readonly",
                     width=12).grid(row=0, column=1)

        tk.Label(frame_form, text="PIN:").grid(row=0, column=2)
        self.__entry_pin = tk.Entry(frame_form, show="*", width=10)
        self.__entry_pin.grid(row=0, column=3)

        tk.Radiobutton(frame_form, text="Ingreso", variable=self.__tipo_var, value="INGRESO").grid(row=0, column=4)
        tk.Radiobutton(frame_form, text="Egreso", variable=self.__tipo_var, value="EGRESO").grid(row=0, column=5)

        tk.Label(frame_form, text="Monto:").grid(row=1, column=0, pady=5)
        self.__entry_monto = tk.Entry(frame_form, width=15)
        self.__entry_monto.grid(row=1, column=1)

        tk.Label(frame_form, text="Concepto:").grid(row=1, column=2)
        self.__entry_concepto = tk.Entry(frame_form, width=20)
        self.__entry_concepto.grid(row=1, column=3)

        frame_btn = tk.Frame(frame_form)
        frame_btn.grid(row=2, column=0, columnspan=6, pady=10)
        tk.Button(frame_btn, text="Registrar", command=self.__registrar).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Actualizar Concepto", command=self.__actualizar).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Eliminar", command=self.__eliminar).pack(side="left", padx=5)

        frame_tabla = tk.Frame(self.__ventana, padx=10, pady=5)
        frame_tabla.pack(fill="both", expand=True)
        col = ("ID", "Tipo", "Monto", "Fecha", "Concepto", "Detalle", "Usuario")
        self.__tabla = ttk.Treeview(frame_tabla, columns=col, show="headings", height=10)
        for c in col:
            self.__tabla.heading(c, text=c)
            self.__tabla.column(c, width=115)
        self.__tabla.pack(fill="both", expand=True)
        self.__tabla.bind("<Double-1>", self.__seleccionar_fila)

    def __cargar_tabla(self):
        for item in self.__tabla.get_children():
            self.__tabla.delete(item)
        for fila in self.__backend.leer_movimientos():
            self.__tabla.insert("", "end", values=fila)

        estado = self.__cuenta.consultar_estado()
        self.__lbl_estado.config(text=estado)
        saldo_num = float(estado.split("$")[1].replace(",", ""))

        self.__meta.actualizar_progreso(saldo_num)
        self.__lbl_meta.config(text=self.__meta.obtener_descripcion())
        self.__barra_progreso["value"] = self.__meta.calcular_porcentaje()

    def __seleccionar_fila(self, event):
        seleccion = self.__tabla.selection()
        if seleccion:
            self.__entry_concepto.delete(0, tk.END)
            self.__entry_concepto.insert(0, self.__tabla.item(seleccion[0], "values")[4])

    def __registrar(self):
        try:
            usr_nom = self.__usuario_var.get()
            usr_obj = self.__usuarios[usr_nom]
            if not usr_obj.validar_pin(self.__entry_pin.get()):
                raise PermissionError("PIN incorrecto.")

            monto = float(self.__entry_monto.get())
            concepto = self.__entry_concepto.get()
            tipo = self.__tipo_var.get()
            id_tx = f"TX-{datetime.now().strftime('%H%M%S')}"
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

            if tipo == "INGRESO":
                self.__cuenta.registrar_ingreso(Deposito(id_tx, monto, fecha, concepto, usr_nom))
            else:
                self.__cuenta.procesar_retiro_o_pago(Egreso(id_tx, monto, fecha, concepto, "Cajero", "General"),
                                                     usr_obj)

            self.__backend.guardar_movimiento(id_tx, tipo, monto, fecha, concepto, "N/A", usr_nom)
            self.__cargar_tabla()
            messagebox.showinfo("Éxito", self.__notificacion.generar_aviso(tipo, monto, concepto, usr_nom))

            self.__entry_monto.delete(0, tk.END)
            self.__entry_concepto.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def __actualizar(self):
        try:
            sel = self.__tabla.selection()
            if not sel: raise ValueError("Seleccione un registro (haga doble clic primero).")
            id_tx = self.__tabla.item(sel[0], "values")[0]
            self.__backend.actualizar_concepto(id_tx, self.__entry_concepto.get())
            self.__cargar_tabla()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def __eliminar(self):
        try:
            sel = self.__tabla.selection()
            if not sel: raise ValueError("Seleccione un registro.")
            id_tx = self.__tabla.item(sel[0], "values")[0]
            if messagebox.askyesno("Confirmar", "¿Eliminar?"):
                self.__backend.eliminar_movimiento(id_tx)
                messagebox.showinfo("Info", "Eliminado. (Reinicie para recalcular el saldo total)")
                self.__cargar_tabla()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def __abrir_ventana_meta(self):
        v = tk.Toplevel(self.__ventana)
        v.title("Meta")
        tk.Label(v, text="Nombre:").pack()
        e_nom = tk.Entry(v)
        e_nom.pack()
        tk.Label(v, text="Monto:").pack()
        e_monto = tk.Entry(v)
        e_monto.pack()

        def guardar():
            try:
                self.__meta.configurar_meta(e_nom.get(), float(e_monto.get()))
                self.__cargar_tabla()
                v.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=v)

        tk.Button(v, text="Guardar", command=guardar).pack()

    def __exportar_reporte(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".txt")
        if ruta:
            self.__reporte.exportar_txt(ruta, self.__cuenta.consultar_estado(), self.__backend.leer_movimientos())
            messagebox.showinfo("Exportado", "Reporte guardado.")

    def iniciar(self):
        self.__ventana.mainloop()