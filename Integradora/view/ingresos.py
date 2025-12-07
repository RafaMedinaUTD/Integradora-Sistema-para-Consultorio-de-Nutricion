# Modulo encargado de controlar la interfaz de ingresos.

import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from model.ingreso import Ingreso
from view.tema import Tema

class VistaIngresos(ctk.CTkFrame):
    def __init__(self, parent, id_admin):
        super().__init__(parent)
        self.id_admin = id_admin
        self.ingreso = Ingreso()
        self.tema = Tema()
        self.configure(fg_color=self.tema.colores["blanco"])
        
        self.configurar_interfaz()
        self.actualizar_lista()
    
    def configurar_interfaz(self): # Metodo encargado de configurar la interfaz.
        # Título de la sección
        titulo = ctk.CTkLabel(self, text="Gestión de Ingresos Diarios", font=("Arial", 28, "bold"), text_color=self.tema.colores["verde"])
        titulo.pack(pady=20)
        
        # Fecha de la sección
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        ctk.CTkLabel(self, text=f"📅 Fecha: {fecha_hoy}", font=("Arial", 18, "bold"), text_color=self.tema.colores["verde"]).pack(pady=5)
        
        # --- Campos de entrada para Formulario ---

        # Frame De Formulario
        form = ctk.CTkFrame(self)
        self.tema.aplicar_tema_frame(form)
        form.pack(fill="x", padx=20, pady=10)
        
        # Entrada de Concepto
        self.tema.crear_texto_pequeno(form, "Concepto:").pack(side="left", padx=10)
        self.concepto_entry = self.tema.crear_entrada(form, "Consulta...", 250)
        self.concepto_entry.pack(side="left", padx=10, pady=10)
        
        # Entrada de Monto
        self.tema.crear_texto_pequeno(form, "Monto ($):").pack(side="left", padx=10)
        self.monto_entry = self.tema.crear_entrada(form, "0.00", 100)
        self.monto_entry.pack(side="left", padx=10, pady=10)
        
        # Boton Registrar
        self.tema.crear_boton_primario(form, "➕ Registrar", self.agregar_ingreso, 150).pack(side="left", padx=20, pady=10)
        
        # Label Total
        self.total_label = ctk.CTkLabel(self, text="Total hoy: $0.00", font=("Arial", 18, "bold"), text_color=self.tema.colores["verde"])
        self.total_label.pack(pady=10)
        
        # --- Tabla de Ingresos ---

        # Vista de ingresos en lista
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Concepto", "Monto", "Hora"), show="headings", height=15)
        self.tree.heading("ID", text="ID"); self.tree.column("ID", width=50)
        self.tree.heading("Concepto", text="Concepto"); self.tree.column("Concepto", width=300)
        self.tree.heading("Monto", text="Monto"); self.tree.column("Monto", width=100)
        self.tree.heading("Hora", text="Hora"); self.tree.column("Hora", width=100)

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Concepto", width=400)
        self.tree.column("Monto", width=150, anchor="e")
        self.tree.column("Hora", width=150, anchor="center")

        self.tree.tag_configure("impar", background=self.tema.colores["gris_claro"])
        self.tree.tag_configure("par", background=self.tema.colores["blanco"])
        
        # Scrollbar para lista
        sb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        
        # --- Botones de Acción ---

        # Frame para botones
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=20, pady=10)
        
        # Boton Editar
        self.tema.crear_boton_primario(btns, "✏️ Editar", self.editar_ingreso, 150).pack(side="left", padx=10)

        # Boton Eliminar
        self.tema.crear_boton_secundario(btns, "🗑️ Eliminar", self.eliminar_ingreso, 150).pack(side="left", padx=10)

        # Boton Reiniciar
        self.tema.crear_boton_secundario(btns, "🔄 Reiniciar Día", self.reiniciar_dia, 150).pack(side="left", padx=10)

        # Boton Refrescar
        self.tema.crear_boton_primario(btns, "🔄 Refrescar", self.actualizar_lista, 150).pack(side="right", padx=10)

    def actualizar_lista(self): # Metodo encargado de actualizar la lista de la tabla dentro de la interfaz.
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            ingresos = self.ingreso.obtener_todos_hoy(self.id_admin)
            total = 0
            for i, ing in enumerate(ingresos):
                tag = "impar" if i % 2 != 0 else "par"
                hora_formateada = str(ing['hora'])[:5] if ing['hora'] else "00:00"
                monto = float(ing['monto'])
                
                self.tree.insert("", "end", values=(
                    ing["id_ingreso"],
                    ing["concepto"],
                    f"${monto:.2f}",
                    hora_formateada
                ), tags=(tag,))
                total += monto
            
            self.total_label.configure(text=f"Total de ingresos hoy: ${total:.2f}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def agregar_ingreso(self): # Metodo encargado de agregar ingresos a la tabla dentro de la interfaz.
        c = self.concepto_entry.get()
        m = self.monto_entry.get()
        if not c or not m: return messagebox.showerror("Error", "Datos incompletos")
        try:
            if float(m) <= 0: raise ValueError
            self.ingreso.crear(c, m, self.id_admin)
            self.actualizar_lista()
            self.concepto_entry.delete(0, "end"); self.monto_entry.delete(0, "end")
        except: messagebox.showerror("Error", "Monto inválido")

    def eliminar_ingreso(self): # Metodo encargado de eliminar ingresos dentro de la interfaz.
        sel = self.tree.selection()
        if not sel: return
        val = self.tree.item(sel[0], "values")
        if messagebox.askyesno("Confirmar", f"¿Eliminar ingreso: {val[1]}?"):
            try: 
                self.ingreso.eliminar(val[0])
                self.actualizar_lista()
            except Exception as e: messagebox.showerror("Error", str(e))

    def reiniciar_dia(self): # Metodo encargado de eliminar todos los registros de ingresos dentro de la interfaz.
        if messagebox.askyesno("PELIGRO", "¿Borrar TODOS los ingresos de hoy?"):
            try:
                self.ingreso.eliminar_todos_hoy(self.id_admin)
                self.actualizar_lista()
            except Exception as e: messagebox.showerror("Error", str(e))
            
    def editar_ingreso(self): # Metodo encargado de actualizar ingresos dentro de la interfaz.
        sel = self.tree.selection()
        if not sel: return messagebox.showerror("Error", "Seleccione un ingreso")
        val = self.tree.item(sel[0], "values")
        
        # Ventana emergente para editar
        popup = ctk.CTkToplevel(self)
        popup.title("Editar Ingreso")
        popup.after(200, lambda: popup.iconbitmap("apple.ico"))
        popup.geometry("300x300")
        popup.grab_set()
        popup.configure(fg_color="white")
        
        self.tema.crear_subtitulo(popup, "Editar Ingreso").pack(pady=10)
        
        # Entrada Concepto
        ce = self.tema.crear_entrada(popup, "Concepto", 200); ce.insert(0, val[1]); ce.pack(pady=5)

        # Entrada Monto
        me = self.tema.crear_entrada(popup, "Monto", 200); me.insert(0, val[2].replace("$","")); me.pack(pady=5)
        
        def guardar(): # Metodo encargado de guardar el ingreso editado.
            try:
                self.ingreso.actualizar(val[0], ce.get(), me.get())
                self.actualizar_lista()
                popup.destroy()
            except Exception as e: messagebox.showerror("Error", str(e))
        
        # Boton Guardar
        self.tema.crear_boton_primario(popup, "Guardar", guardar, 150).pack(pady=10)