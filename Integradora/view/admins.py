# Modulo encargado de controlar la interfaz de administradores.

import customtkinter as ctk
from tkinter import ttk, messagebox
from model.administrador import Administrador
from view.tema import Tema
from controller.validaciones import Validaciones

class VistaAdmins(ctk.CTkFrame):
    def __init__(self, parent, id_admin_actual):
        super().__init__(parent)
        self.id_admin_actual = id_admin_actual
        self.administrador = Administrador()
        self.tema = Tema()
        
        self.configure(fg_color=self.tema.colores["blanco"])
        
        self.configurar_interfaz()
        self.actualizar_lista()
    
    def configurar_interfaz(self): # Metodo encargado de configurar la interfaz.
        # Título de la sección
        titulo = ctk.CTkLabel(
            self,
            text="Gestión de Administradores",
            font=("Arial", 28, "bold"),
            text_color=self.tema.colores["verde"]
        )
        titulo.pack(pady=20)
        
        # --- Campos de entrada para Formulario ---

        # Frame De Formulario
        form_frame = ctk.CTkFrame(self)
        self.tema.aplicar_tema_frame(form_frame)
        form_frame.pack(fill="x", padx=20, pady=10)

        # Nombre
        self.tema.crear_texto_pequeno(form_frame, "Nombre:").pack(side="left", padx=10)
        self.nombre_entry = self.tema.crear_entrada(form_frame, "Nombre completo", 200)
        self.nombre_entry.pack(side="left", padx=10, pady=15)
        
        # Teléfono
        self.tema.crear_texto_pequeno(form_frame, "Teléfono:").pack(side="left", padx=10)
        self.telefono_entry = self.tema.crear_entrada(form_frame, "10 dígitos", 120)
        self.telefono_entry.pack(side="left", padx=10, pady=15)
        
        # Correo
        self.tema.crear_texto_pequeno(form_frame, "Correo:").pack(side="left", padx=10)
        self.correo_entry = self.tema.crear_entrada(form_frame, "ejemplo@email.com", 200)
        self.correo_entry.pack(side="left", padx=10, pady=15)
        
        # Contraseña
        self.tema.crear_texto_pequeno(form_frame, "Contraseña:").pack(side="left", padx=10)
        self.contrasena_entry = self.tema.crear_entrada(form_frame, "******", 120)
        self.contrasena_entry.configure(show="•")
        self.contrasena_entry.pack(side="left", padx=10, pady=15)
        
        # Botón Agregar
        self.boton_agregar = self.tema.crear_boton_primario(form_frame, "➕ Agregar Admin", self.agregar_admin, 150)
        self.boton_agregar.pack(side="left", padx=20, pady=15)
        
        # --- Tabla de Administradores ---

        # Vista de administradores en lista
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Nombre", "Teléfono", "Correo", "Estado"), show="headings", height=15)
        self.tree.configure()
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Correo", text="Correo")
        self.tree.heading("Estado", text="Estado")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=250)
        self.tree.column("Teléfono", width=120, anchor="center")
        self.tree.column("Correo", width=200)
        self.tree.column("Estado", width=80, anchor="center")

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
        
        # Botón Editar
        self.boton_editar = self.tema.crear_boton_primario(button_frame, "✏️ Editar", self.editar_admin, 150)
        self.boton_editar.pack(side="left", padx=10)
        
        # Botón Reactivar
        self.boton_reactivar = self.tema.crear_boton_primario(button_frame, "🔄 Reactivar", self.reactivar_admin, 150)
        self.boton_reactivar.pack(side="left", padx=10)
        
        # Botón Eliminar
        self.boton_eliminar = self.tema.crear_boton_secundario(button_frame, "🗑️ Eliminar", self.eliminar_admin, 150)
        self.boton_eliminar.pack(side="left", padx=10)
        
        # Botón Actualizar
        self.boton_actualizar = self.tema.crear_boton_primario(button_frame, "🔄 Refrescar Lista", self.actualizar_lista, 150)
        self.boton_actualizar.pack(side="right", padx=10)
    
    def actualizar_lista(self): # Metodo encargado de actualizar la lista dentro de la interfaz.
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            administradores = self.administrador.obtener_todos()
            for i, admin in enumerate(administradores):
                estado = "Activo" if admin.get("activo", 1) else "Inactivo"
                tag = "impar" if i % 2 != 0 else "par"
                
                self.tree.insert("", "end", values=(
                    admin["id_administrador"],
                    admin["nombre"],
                    admin["telefono"],
                    admin["correo"],
                    estado
                ), tags=(tag,))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar administradores: {str(e)}")
    
    def agregar_admin(self): # Metodo encargado de agregar nuevos administradores dentro de la interfaz.
        nombre = self.nombre_entry.get()
        telefono = self.telefono_entry.get()
        correo = self.correo_entry.get()
        contrasena = self.contrasena_entry.get()
        
        if not all([nombre, telefono, correo, contrasena]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if not Validaciones.validar_correo(correo):
            messagebox.showerror("Error", "Formato de correo inválido")
            return
        
        if not Validaciones.validar_telefono(telefono):
            messagebox.showerror("Error", "Teléfono debe tener al menos 10 dígitos")
            return
        
        try:
            if self.administrador.verificar_correo_existente(correo):
                messagebox.showerror("Error", "El correo ya está registrado")
                return
            
            self.administrador.registrar(nombre, telefono, correo, contrasena)
            self.actualizar_lista()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Administrador agregado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def editar_admin(self): # Metodo encargado de editar administradores existentes dentro de la interfaz.
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un administrador")
            return
        
        item = seleccionado[0]
        valores = self.tree.item(item, "values")
        
        # Ventana emergente para editar
        ventana_editar = ctk.CTkToplevel(self)
        ventana_editar.title("Editar Administrador")
        ventana_editar.after(200, lambda: ventana_editar.iconbitmap("apple.ico"))
        ventana_editar.geometry("400x500")
        ventana_editar.resizable(False, False)
        ventana_editar.grab_set()
        ventana_editar.configure(fg_color=self.tema.colores["blanco"])
        
        # Centrar la ventana emergente
        ventana_editar.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        ventana_editar.geometry(f"400x500+{x}+{y}")
        
        # Titulo de la ventana emergente
        titulo = self.tema.crear_subtitulo(ventana_editar, "Editar Administrador")
        titulo.pack(pady=20)
        
        # Nombre
        nombre_entry = self.tema.crear_entrada(ventana_editar, "Nombre", 300)
        nombre_entry.insert(0, valores[1])
        nombre_entry.pack(pady=10)
        
        # Telefono
        telefono_entry = self.tema.crear_entrada(ventana_editar, "Teléfono", 300)
        telefono_entry.insert(0, valores[2])
        telefono_entry.pack(pady=10)
        
        # Correo
        correo_entry = self.tema.crear_entrada(ventana_editar, "Correo", 300)
        correo_entry.insert(0, valores[3])
        correo_entry.configure(state="disabled") # No editable
        correo_entry.pack(pady=10)
        
        # Contraseña
        contrasena_entry = self.tema.crear_entrada(ventana_editar, "Nueva contraseña (opcional)", 300)
        contrasena_entry.configure(show="•")
        contrasena_entry.pack(pady=10)
        
        def guardar_cambios(): # Meotdo encargado de guardar los cambios
            nuevo_nombre = nombre_entry.get()
            nuevo_telefono = telefono_entry.get()
            nueva_contrasena = contrasena_entry.get()
            
            if not nuevo_nombre or not nuevo_telefono:
                messagebox.showerror("Error", "Nombre y teléfono obligatorios")
                return
            
            if not Validaciones.validar_telefono(nuevo_telefono):
                messagebox.showerror("Error", "Teléfono inválido")
                return
            
            try:
                self.administrador.actualizar(valores[0], nuevo_nombre, nuevo_telefono, nueva_contrasena)
                self.actualizar_lista()
                ventana_editar.destroy()
                messagebox.showinfo("Éxito", "Administrador actualizado")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        # Boton para guardar
        self.tema.crear_boton_primario(ventana_editar, "💾 Guardar Cambios", guardar_cambios, 200).pack(pady=20)
    
    def eliminar_admin(self): # Metodo encargado de eliminar (desactivar) administradores existentes dentro de la interfaz.
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un administrador")
            return
        
        item = seleccionado[0]
        valores = self.tree.item(item, "values")
        id_admin = valores[0]
        
        if int(id_admin) == self.id_admin_actual:
            messagebox.showerror("Error", "No puede eliminarse a sí mismo")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar al administrador: {valores[1]}?"):
            try:
                self.administrador.eliminar(id_admin)
                self.actualizar_lista()
                messagebox.showinfo("Éxito", "Administrador eliminado")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def reactivar_admin(self): # Metodo encargado de reactivar administradores existentes dentro de la interfaz.
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un administrador")
            return
        
        item = seleccionado[0]
        valores = self.tree.item(item, "values")
        
        if valores[4] == "Activo":
            messagebox.showwarning("Aviso", "Este administrador ya está activo")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Reactivar al administrador: {valores[1]}?"):
            try:
                self.administrador.reactivar(valores[0])
                self.actualizar_lista()
                messagebox.showinfo("Éxito", "Administrador reactivado")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def limpiar_campos(self): # Metodo limpiar los campos dentro de la interfaz.
        self.nombre_entry.delete(0, "end")
        self.telefono_entry.delete(0, "end")
        self.correo_entry.delete(0, "end")
        self.contrasena_entry.delete(0, "end")