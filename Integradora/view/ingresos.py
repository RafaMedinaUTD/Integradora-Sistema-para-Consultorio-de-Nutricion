import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from model.ingreso import Ingreso
from view.tema import Tema
from configuracion import Configuracion

class VentanaIngresos:
    def __init__(self, ventana_principal, id_admin):
        self.ventana_principal = ventana_principal
        self.id_admin = id_admin
        self.ingreso = Ingreso()
        self.tema = Tema()
        
        self.ventana = ctk.CTkToplevel(ventana_principal)
        self.ventana.title("Gestión de Ingresos")
        
        # Configurar pantalla completa
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        self.ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
        self.ventana.attributes('-fullscreen', True)
        
        self.ventana.configure(fg_color=self.tema.colores["blanco"])
        self.ventana.protocol("WM_DELETE_WINDOW", self.volver_principal)
        
        # Configurar atajo de teclado para salir de pantalla completa (Esc)
        self.ventana.bind('<Escape>', lambda e: self.volver_principal())
        
        self.configurar_interfaz()
        self.actualizar_lista()
        self.ventana.focus_set()
    
    def configurar_interfaz(self):
        header_frame = ctk.CTkFrame(self.ventana, fg_color=self.tema.colores["verde"], height=100)
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        titulo = ctk.CTkLabel(
            header_frame,
            text="Gestión de Ingresos Diarios",
            font=("Arial", 28, "bold"),
            text_color=self.tema.colores["blanco"]
        )
        titulo.pack(pady=25)
        
        # Frame para fecha actual
        fecha_frame = ctk.CTkFrame(self.ventana)
        fecha_frame.pack(fill="x", padx=20, pady=10)
        
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        fecha_label = ctk.CTkLabel(
            fecha_frame,
            text=f"📅 Fecha: {fecha_hoy}",
            font=("Arial", 18, "bold"),
            text_color=self.tema.colores["verde"]
        )
        fecha_label.pack(pady=10)
        
        form_frame = ctk.CTkFrame(self.ventana)
        self.tema.aplicar_tema_frame(form_frame)
        form_frame.pack(fill="x", padx=20, pady=15)
        
        self.texto_concepto = self.tema.crear_texto_pequeno(form_frame, "Concepto:")
        self.texto_concepto.pack(side="left", padx=15)
        self.concepto_entry = self.tema.crear_entrada(form_frame, "Ej: Consulta, Producto, etc.", 300)
        self.concepto_entry.pack(side="left", padx=15, pady=15)
        
        self.texto_monto = self.tema.crear_texto_pequeno(form_frame, "Monto ($):")
        self.texto_monto.pack(side="left", padx=15)
        self.monto_entry = self.tema.crear_entrada(form_frame, "0.00", 150)
        self.monto_entry.pack(side="left", padx=15, pady=15)
        
        self.boton_agregar = self.tema.crear_boton_primario(form_frame, "➕ AGREGAR INGRESO", self.agregar_ingreso, 200)
        self.boton_agregar.pack(side="left", padx=15, pady=15)
        
        # Frame para estadísticas
        stats_frame = ctk.CTkFrame(self.ventana)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        self.total_label = ctk.CTkLabel(
            stats_frame,
            text="Total de ingresos hoy: $0.00",
            font=("Arial", 18, "bold"),
            text_color=self.tema.colores["verde"]
        )
        self.total_label.pack(pady=10)
        
        self.tree_frame = ctk.CTkFrame(self.ventana)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Concepto", "Monto", "Hora"), show="headings", height=20)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Concepto", text="Concepto")
        self.tree.heading("Monto", text="Monto ($)")
        self.tree.heading("Hora", text="Hora")
        self.tree.column("ID", width=80)
        self.tree.column("Concepto", width=400)
        self.tree.column("Monto", width=150)
        self.tree.column("Hora", width=150)
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        button_frame = ctk.CTkFrame(self.ventana)
        button_frame.pack(fill="x", padx=20, pady=15)
        
        self.boton_volver = self.tema.crear_boton_primario(button_frame, "← VOLVER AL MENÚ", self.volver_principal, 250)
        self.boton_volver.pack(side="left", padx=10)
        
        self.boton_editar = self.tema.crear_boton_primario(button_frame, "✏️ EDITAR INGRESO", self.editar_ingreso, 200)
        self.boton_editar.pack(side="left", padx=10)
        
        self.boton_eliminar = self.tema.crear_boton_secundario(button_frame, "🗑️ ELIMINAR INGRESO", self.eliminar_ingreso, 200)
        self.boton_eliminar.pack(side="left", padx=10)
        
        self.boton_reiniciar = self.tema.crear_boton_secundario(button_frame, "🔄 REINICIAR DÍA", self.reiniciar_dia, 200)
        self.boton_reiniciar.pack(side="left", padx=10)
        
        self.boton_actualizar = self.tema.crear_boton_primario(button_frame, "🔄 ACTUALIZAR LISTA", self.actualizar_lista, 200)
        self.boton_actualizar.pack(side="right", padx=10)
    
    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            ingresos = self.ingreso.obtener_todos_hoy(self.id_admin)
            total = 0
            for ing in ingresos:
                # Formatear hora
                hora_formateada = str(ing['hora'])[:5] if ing['hora'] else "00:00"
                self.tree.insert("", "end", values=(
                    ing["id_ingreso"],
                    ing["concepto"],
                    f"${float(ing['monto']):.2f}",
                    hora_formateada
                ))
                total += float(ing['monto'])
            
            self.total_label.configure(text=f"Total de ingresos hoy: ${total:.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ingresos: {str(e)}")
    
    def agregar_ingreso(self):
        concepto = self.concepto_entry.get()
        monto = self.monto_entry.get()
        
        if not concepto or not monto:
            messagebox.showerror("Error", "Concepto y monto son obligatorios")
            return
        
        try:
            monto_float = float(monto)
            if monto_float <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a 0")
                return
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido")
            return
        
        try:
            self.ingreso.crear(concepto, monto, self.id_admin)
            self.actualizar_lista()
            self.concepto_entry.delete(0, "end")
            self.monto_entry.delete(0, "end")
            messagebox.showinfo("Éxito", "Ingreso agregado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def editar_ingreso(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un ingreso")
            return
        
        item = seleccionado[0]
        valores = self.tree.item(item, "values")
        
        ventana_editar = ctk.CTkToplevel(self.ventana)
        ventana_editar.title("Editar Ingreso")
        ventana_editar.geometry("400x300")
        ventana_editar.resizable(False, False)
        ventana_editar.grab_set()
        self.centrar_ventana_secundaria(ventana_editar, "400x300")
        
        titulo = self.tema.crear_subtitulo(ventana_editar, "Editar Ingreso")
        titulo.pack(pady=20)
        
        concepto_entry = self.tema.crear_entrada(ventana_editar, "Concepto", 300)
        concepto_entry.insert(0, valores[1])
        concepto_entry.pack(pady=10)
        
        monto_entry = self.tema.crear_entrada(ventana_editar, "Monto", 300)
        monto_text = valores[2].replace("$", "")
        monto_entry.insert(0, monto_text)
        monto_entry.pack(pady=10)
        
        def guardar_cambios():
            nuevo_concepto = concepto_entry.get()
            nuevo_monto = monto_entry.get()
            
            if not nuevo_concepto or not nuevo_monto:
                messagebox.showerror("Error", "Concepto y monto son obligatorios")
                return
            
            try:
                monto_float = float(nuevo_monto)
                if monto_float <= 0:
                    messagebox.showerror("Error", "El monto debe ser mayor a 0")
                    return
            except ValueError:
                messagebox.showerror("Error", "El monto debe ser un número válido")
                return
            
            try:
                self.ingreso.actualizar(valores[0], nuevo_concepto, nuevo_monto)
                self.actualizar_lista()
                ventana_editar.destroy()
                messagebox.showinfo("Éxito", "Ingreso actualizado correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        boton_guardar = self.tema.crear_boton_primario(ventana_editar, "💾 GUARDAR", guardar_cambios, 200)
        boton_guardar.pack(pady=15)
    
    def centrar_ventana_secundaria(self, ventana, tamanio):
        ventana.update_idletasks()
        ancho = int(tamanio.split('x')[0])
        alto = int(tamanio.split('x')[1])
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"{tamanio}+{x}+{y}")
    
    def eliminar_ingreso(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un ingreso")
            return
        
        item = seleccionado[0]
        valores = self.tree.item(item, "values")
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el ingreso: {valores[1]}?"):
            try:
                self.ingreso.eliminar(valores[0])
                self.actualizar_lista()
                messagebox.showinfo("Éxito", "Ingreso eliminado correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def reiniciar_dia(self):
        if messagebox.askyesno("Confirmar", "⚠️ ¿Está seguro de reiniciar el día?\n\nEsta acción eliminará TODOS los ingresos registrados hoy y no se puede deshacer."):
            try:
                self.ingreso.eliminar_todos_hoy(self.id_admin)
                self.actualizar_lista()
                messagebox.showinfo("Éxito", "Ingresos del día reiniciados correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def volver_principal(self):
        self.ventana.attributes('-fullscreen', False)
        self.ventana.destroy()
        self.ventana_principal.deiconify()