# Modulo encargado de controlar la interfaz de pacientes.

import customtkinter as ctk
from tkinter import ttk, messagebox
from model.paciente import Paciente
from view.tema import Tema

class VistaPacientes(ctk.CTkFrame):
    def __init__(self, parent, id_admin):
        super().__init__(parent) # Inicializar como Frame
        self.id_admin = id_admin
        self.paciente = Paciente()
        self.tema = Tema()
        
        # Configuración visual del Frame
        self.configure(fg_color=self.tema.colores["blanco"])
        
        self.configurar_interfaz()
        self.actualizar_lista()
    
    def configurar_interfaz(self): # Metodo encargado de configurar la interfaz.
        # Titulo de la sección
        titulo = ctk.CTkLabel(
            self,
            text="Gestión de Pacientes",
            font=("Arial", 28, "bold"),
            text_color=self.tema.colores["verde"]
        )
        titulo.pack(pady=20)
        
        # --- Campos de entrada para Formulario ---

        # Frame De Login
        form_frame = ctk.CTkFrame(self)
        self.tema.aplicar_tema_frame(form_frame)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        # Nombre
        self.texto_nombre = self.tema.crear_texto_pequeno(form_frame, "Nombre:")
        self.texto_nombre.pack(side="left", padx=10)
        self.nombre_entry = self.tema.crear_entrada(form_frame, "Nombre completo", 200)
        self.nombre_entry.pack(side="left", padx=10, pady=15)
        
        # Dieta
        self.texto_dieta = self.tema.crear_texto_pequeno(form_frame, "Dieta:")
        self.texto_dieta.pack(side="left", padx=10)
        self.dieta_entry = self.tema.crear_entrada(form_frame, "Tipo Dieta", 150)
        self.dieta_entry.pack(side="left", padx=10, pady=15)
        
        # Peso
        self.texto_peso = self.tema.crear_texto_pequeno(form_frame, "Peso (kg):")
        self.texto_peso.pack(side="left", padx=10)
        self.peso_entry = self.tema.crear_entrada(form_frame, "0.00", 80)
        self.peso_entry.pack(side="left", padx=10, pady=15)
        
        # Boton Agregar
        self.boton_agregar = self.tema.crear_boton_primario(form_frame, "➕ Agregar", self.agregar_paciente, 120)
        self.boton_agregar.pack(side="left", padx=15, pady=15)
        
        # Tabla (Treeview)
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Estilo Treeview (Truco para modo oscuro/claro si fuera necesario, usando default por ahora)
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        
        # --- Tabla de Pacientes ---

        # Vista de pacientes en lista
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Nombre", "Dieta", "Peso"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre del Paciente")
        self.tree.heading("Dieta", text="Tipo de Dieta")
        self.tree.heading("Peso", text="Peso (kg)")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=300, anchor="center")
        self.tree.column("Dieta", width=250, anchor="center")
        self.tree.column("Peso", width=100, anchor="center")
        
        self.tree.tag_configure("impar", background=self.tema.colores["gris_claro"])
        self.tree.tag_configure("par", background=self.tema.colores["blanco"])
        
        # Scrollbar para lista
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- Botones de Acción ---

        # Frame para botones
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=15)
        
        # Boton Editar
        self.boton_editar = self.tema.crear_boton_primario(button_frame, "✏️ Editar Seleccionado", self.editar_paciente, 200)
        self.boton_editar.pack(side="left", padx=10)
        
        # Boton Eliminar
        self.boton_eliminar = self.tema.crear_boton_secundario(button_frame, "🗑️ Eliminar Seleccionado", self.eliminar_paciente, 200)
        self.boton_eliminar.pack(side="left", padx=10)
        
        # Boton Actualizar
        self.boton_actualizar = self.tema.crear_boton_primario(button_frame, "🔄 Recargar Lista", self.actualizar_lista, 150)
        self.boton_actualizar.pack(side="right", padx=10)
    
    def actualizar_lista(self): # Metodo encargado de actualizar la lista en la interfaz.
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            pacientes = self.paciente.obtener_todos(self.id_admin)
            for i, paciente in enumerate(pacientes):
                tag = "impar" if i % 2 != 0 else "par"
                
                self.tree.insert("", "end", values=(
                    paciente["id_paciente"],
                    paciente["nombre"],
                    paciente["dieta"],
                    paciente["peso"]
                ), tags=(tag,))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pacientes: {str(e)}")

    def agregar_paciente(self): # Metodo encargado de agregar pacientes en la interfaz.
        nombre = self.nombre_entry.get()
        dieta = self.dieta_entry.get()
        peso = self.peso_entry.get()
        if not nombre or not dieta:
            messagebox.showerror("Error", "Nombre y dieta son obligatorios")
            return
        if peso:
            try: float(peso)
            except ValueError:
                messagebox.showerror("Error", "El peso debe ser un número válido")
                return
        try:
            self.paciente.crear(nombre, dieta, peso, self.id_admin)
            self.actualizar_lista()
            self.nombre_entry.delete(0, "end")
            self.dieta_entry.delete(0, "end")
            self.peso_entry.delete(0, "end")
            messagebox.showinfo("Éxito", "Paciente agregado correctamente")
        except Exception as e: messagebox.showerror("Error", str(e))

    def editar_paciente(self): # Metodo encargado de editar pacientes en la interfaz.
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un paciente")
            return
        item = seleccionado[0]
        valores = self.tree.item(item, "values")
        
        # Ventana emergente para editar
        ventana_editar = ctk.CTkToplevel(self)
        ventana_editar.title("Editar Paciente")
        ventana_editar.after(200, lambda: ventana_editar.iconbitmap("apple.ico"))
        ventana_editar.geometry("400x400")
        ventana_editar.grab_set() # Modal
        
        # Centrar ventana emergente
        ventana_editar.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (400 // 2)
        ventana_editar.geometry(f"400x400+{x}+{y}")
        ventana_editar.configure(fg_color=self.tema.colores["blanco"])

        # Label Titulo
        titulo = self.tema.crear_subtitulo(ventana_editar, "Editar Paciente")
        titulo.pack(pady=20)
        
        # Entrada Nombre
        nombre_entry = self.tema.crear_entrada(ventana_editar, "Nombre", 300)
        nombre_entry.insert(0, valores[1])
        nombre_entry.pack(pady=10)

        # Entrada Dieta
        dieta_entry = self.tema.crear_entrada(ventana_editar, "Dieta", 300)
        dieta_entry.insert(0, valores[2])
        dieta_entry.pack(pady=10)

        # Entrada Peso
        peso_entry = self.tema.crear_entrada(ventana_editar, "Peso (kg)", 300)
        peso_entry.insert(0, valores[3])
        peso_entry.pack(pady=10)
        
        def guardar_cambios(): # Metodo encargado de guardar los cambios.
            nuevo_nombre = nombre_entry.get()
            nueva_dieta = dieta_entry.get()
            nuevo_peso = peso_entry.get()
            if not nuevo_nombre or not nueva_dieta:
                messagebox.showerror("Error", "Campos obligatorios")
                return
            if nuevo_peso:
                try: float(nuevo_peso)
                except ValueError:
                    messagebox.showerror("Error", "Peso inválido")
                    return
            try:
                self.paciente.actualizar(valores[0], nuevo_nombre, nueva_dieta, nuevo_peso)
                self.actualizar_lista()
                ventana_editar.destroy()
                messagebox.showinfo("Éxito", "Actualizado")
            except Exception as e: messagebox.showerror("Error", str(e))
        
        # Boton Guardar
        self.tema.crear_boton_primario(ventana_editar, "💾 Guardar", guardar_cambios, 200).pack(pady=15)

    def eliminar_paciente(self): # Metodo encargado de eliminar pacientes en la interfaz.
        # Lógica idéntica al original
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un paciente")
            return
        item = seleccionado[0]
        valores = self.tree.item(item, "values")
        nombre_paciente = valores[1]
        id_paciente = valores[0]
        
        try:
            pacientes_con_citas = self.paciente.obtener_con_citas(self.id_admin)
            tiene_citas = any(str(p['id_paciente']) == str(id_paciente) and p.get('total_citas', 0) > 0 for p in pacientes_con_citas)
        except: tiene_citas = False
        
        mensaje = f"¿Eliminar a {nombre_paciente}?"
        if tiene_citas: mensaje += "\n\n⚠️ ADVERTENCIA: Se eliminarán sus citas programadas."
        
        if messagebox.askyesno("Confirmar Eliminación", mensaje):
            try:
                self.paciente.eliminar(id_paciente)
                self.actualizar_lista()
                messagebox.showinfo("Éxito", "Paciente eliminado")
            except Exception as e: messagebox.showerror("Error", str(e))