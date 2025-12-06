import customtkinter as ctk
from tkinter import ttk, messagebox
from model.paciente import Paciente
from view.tema import Tema
from configuracion import Configuracion

class VentanaPacientes:
    def __init__(self, ventana_principal, id_admin):
        self.ventana_principal = ventana_principal
        self.id_admin = id_admin
        self.paciente = Paciente()
        self.tema = Tema()
        
        self.ventana = ctk.CTkToplevel(ventana_principal)
        self.ventana.title("Gestión de Pacientes")
        
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
        # Header más grande para pantalla completa
        header_frame = ctk.CTkFrame(self.ventana, fg_color=self.tema.colores["verde"], height=100)
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        titulo = ctk.CTkLabel(
            header_frame,
            text="Gestión de Pacientes",
            font=("Arial", 28, "bold"),
            text_color=self.tema.colores["blanco"]
        )
        titulo.pack(pady=25)
        
        # Form frame más grande
        form_frame = ctk.CTkFrame(self.ventana)
        self.tema.aplicar_tema_frame(form_frame)
        form_frame.pack(fill="x", padx=20, pady=15)
        
        # Campos más grandes para pantalla completa
        self.texto_nombre = self.tema.crear_texto_pequeno(form_frame, "Nombre del paciente:")
        self.texto_nombre.pack(side="left", padx=15)
        self.nombre_entry = self.tema.crear_entrada(form_frame, "Nombre", 250)
        self.nombre_entry.pack(side="left", padx=15, pady=15)
        
        self.texto_dieta = self.tema.crear_texto_pequeno(form_frame, "Tipo de dieta:")
        self.texto_dieta.pack(side="left", padx=15)
        self.dieta_entry = self.tema.crear_entrada(form_frame, "Tipo Dieta", 200)
        self.dieta_entry.pack(side="left", padx=15, pady=15)
        
        self.texto_peso = self.tema.crear_texto_pequeno(form_frame, "Peso (kg):")
        self.texto_peso.pack(side="left", padx=15)
        self.peso_entry = self.tema.crear_entrada(form_frame, "Peso (kg)", 150)
        self.peso_entry.pack(side="left", padx=15, pady=15)
        
        self.boton_agregar = self.tema.crear_boton_primario(form_frame, "➕ AGREGAR PACIENTE", self.agregar_paciente, 200)
        self.boton_agregar.pack(side="left", padx=15, pady=15)
        
        # Treeview más grande
        self.tree_frame = ctk.CTkFrame(self.ventana)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Nombre", "Dieta", "Peso"), show="headings", height=20)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre del Paciente")
        self.tree.heading("Dieta", text="Tipo de Dieta")
        self.tree.heading("Peso", text="Peso (kg)")
        self.tree.column("ID", width=100)
        self.tree.column("Nombre", width=400)
        self.tree.column("Dieta", width=300)
        self.tree.column("Peso", width=200)
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones más grandes
        button_frame = ctk.CTkFrame(self.ventana)
        button_frame.pack(fill="x", padx=20, pady=15)
        
        self.boton_volver = self.tema.crear_boton_primario(button_frame, "← VOLVER AL MENÚ", self.volver_principal, 250)
        self.boton_volver.pack(side="left", padx=10)
        
        self.boton_editar = self.tema.crear_boton_primario(button_frame, "✏️ EDITAR PACIENTE", self.editar_paciente, 200)
        self.boton_editar.pack(side="left", padx=10)
        
        self.boton_eliminar = self.tema.crear_boton_secundario(button_frame, "🗑️ ELIMINAR PACIENTE", self.eliminar_paciente, 200)
        self.boton_eliminar.pack(side="left", padx=10)
        
        self.boton_actualizar = self.tema.crear_boton_primario(button_frame, "🔄 ACTUALIZAR LISTA", self.actualizar_lista, 200)
        self.boton_actualizar.pack(side="right", padx=10)
    
    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            pacientes = self.paciente.obtener_todos(self.id_admin)
            for paciente in pacientes:
                self.tree.insert("", "end", values=(
                    paciente["id_paciente"],
                    paciente["nombre"],
                    paciente["dieta"],
                    paciente["peso"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pacientes: {str(e)}")
    
    def agregar_paciente(self):
        nombre = self.nombre_entry.get()
        dieta = self.dieta_entry.get()
        peso = self.peso_entry.get()
        
        if not nombre or not dieta:
            messagebox.showerror("Error", "Nombre y dieta son obligatorios")
            return
        
        # Validar que el peso sea un número si se proporciona
        if peso:
            try:
                float(peso)
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
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def editar_paciente(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un paciente")
            return
        
        item = seleccionado[0]
        valores = self.tree.item(item, "values")
        
        ventana_editar = ctk.CTkToplevel(self.ventana)
        ventana_editar.title("Editar Paciente")
        ventana_editar.geometry("400x400")
        ventana_editar.resizable(False, False)
        ventana_editar.grab_set()
        self.centrar_ventana_secundaria(ventana_editar, "400x400")
        
        titulo = self.tema.crear_subtitulo(ventana_editar, "Editar Paciente")
        titulo.pack(pady=20)
        
        nombre_entry = self.tema.crear_entrada(ventana_editar, "Nombre", 300)
        nombre_entry.insert(0, valores[1])
        nombre_entry.pack(pady=10)
        
        dieta_entry = self.tema.crear_entrada(ventana_editar, "Dieta", 300)
        dieta_entry.insert(0, valores[2])
        dieta_entry.pack(pady=10)
        
        peso_entry = self.tema.crear_entrada(ventana_editar, "Peso (kg)", 300)
        peso_entry.insert(0, valores[3])
        peso_entry.pack(pady=10)
        
        def guardar_cambios():
            nuevo_nombre = nombre_entry.get()
            nueva_dieta = dieta_entry.get()
            nuevo_peso = peso_entry.get()
            
            if not nuevo_nombre or not nueva_dieta:
                messagebox.showerror("Error", "Nombre y dieta son obligatorios")
                return
            
            # Validar peso
            if nuevo_peso:
                try:
                    float(nuevo_peso)
                except ValueError:
                    messagebox.showerror("Error", "El peso debe ser un número válido")
                    return
            
            try:
                self.paciente.actualizar(valores[0], nuevo_nombre, nueva_dieta, nuevo_peso)
                self.actualizar_lista()
                ventana_editar.destroy()
                messagebox.showinfo("Éxito", "Paciente actualizado correctamente")
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
    
    def eliminar_paciente(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un paciente")
            return
        
        item = seleccionado[0]
        valores = self.tree.item(item, "values")
        nombre_paciente = valores[1]
        id_paciente = valores[0]
        
        # Verificar si el paciente tiene citas activas
        try:
            pacientes_con_citas = self.paciente.obtener_con_citas(self.id_admin)
            tiene_citas = False
            for paciente in pacientes_con_citas:
                if paciente['id_paciente'] == id_paciente and paciente.get('total_citas', 0) > 0:
                    tiene_citas = True
                    break
        except:
            tiene_citas = False
        
        if tiene_citas:
            mensaje = f"¿Está seguro de eliminar al paciente: {nombre_paciente}?\n\n⚠️ ADVERTENCIA: Este paciente tiene citas programadas. Al eliminarlo, también se eliminarán todas sus citas."
        else:
            mensaje = f"¿Está seguro de eliminar al paciente: {nombre_paciente}?"
        
        if messagebox.askyesno("Confirmar Eliminación", mensaje):
            try:
                self.paciente.eliminar(id_paciente)
                self.actualizar_lista()
                messagebox.showinfo("Éxito", "Paciente eliminado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el paciente: {str(e)}")
    
    def volver_principal(self):
        self.ventana.attributes('-fullscreen', False)
        self.ventana.destroy()
        self.ventana_principal.deiconify()