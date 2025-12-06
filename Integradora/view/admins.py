import customtkinter as ctk
from tkinter import ttk, messagebox
from model.administrador import Administrador
from view.tema import Tema
from configuracion import Configuracion
from controller.validaciones import Validaciones

class VentanaAdmins:
    def __init__(self, ventana_principal, id_admin_actual):
        self.ventana_principal = ventana_principal
        self.id_admin_actual = id_admin_actual
        self.administrador = Administrador()
        self.tema = Tema()
        
        self.ventana = ctk.CTkToplevel(ventana_principal)
        self.ventana.title("Gestión de Administradores")
        
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
            text="Gestión de Administradores",
            font=("Arial", 28, "bold"),
            text_color=self.tema.colores["blanco"]
        )
        titulo.pack(pady=25)
        
        form_frame = ctk.CTkFrame(self.ventana)
        self.tema.aplicar_tema_frame(form_frame)
        form_frame.pack(fill="x", padx=20, pady=15)
        
        self.texto_nombre = self.tema.crear_texto_pequeno(form_frame, "Nombre:")
        self.texto_nombre.pack(side="left", padx=15)
        self.nombre_entry = self.tema.crear_entrada(form_frame, "Nombre completo", 200)
        self.nombre_entry.pack(side="left", padx=15, pady=15)
        
        self.texto_telefono = self.tema.crear_texto_pequeno(form_frame, "Teléfono:")
        self.texto_telefono.pack(side="left", padx=15)
        self.telefono_entry = self.tema.crear_entrada(form_frame, "1234567890", 150)
        self.telefono_entry.pack(side="left", padx=15, pady=15)
        
        self.texto_correo = self.tema.crear_texto_pequeno(form_frame, "Correo:")
        self.texto_correo.pack(side="left", padx=15)
        self.correo_entry = self.tema.crear_entrada(form_frame, "ejemplo@email.com", 200)
        self.correo_entry.pack(side="left", padx=15, pady=15)
        
        self.texto_contrasena = self.tema.crear_texto_pequeno(form_frame, "Contraseña:")
        self.texto_contrasena.pack(side="left", padx=15)
        self.contrasena_entry = self.tema.crear_entrada(form_frame, "******", 150)
        self.contrasena_entry.configure(show="•")
        self.contrasena_entry.pack(side="left", padx=15, pady=15)
        
        self.boton_agregar = self.tema.crear_boton_primario(form_frame, "➕ AGREGAR ADMIN", self.agregar_admin, 200)
        self.boton_agregar.pack(side="left", padx=15, pady=15)
        
        self.tree_frame = ctk.CTkFrame(self.ventana)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Nombre", "Teléfono", "Correo", "Estado"), show="headings", height=20)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Correo", text="Correo")
        self.tree.heading("Estado", text="Estado")
        self.tree.column("ID", width=80)
        self.tree.column("Nombre", width=300)
        self.tree.column("Teléfono", width=150)
        self.tree.column("Correo", width=250)
        self.tree.column("Estado", width=100)
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        button_frame = ctk.CTkFrame(self.ventana)
        button_frame.pack(fill="x", padx=20, pady=15)
        
        self.boton_volver = self.tema.crear_boton_primario(button_frame, "← VOLVER AL MENÚ", self.volver_principal, 250)
        self.boton_volver.pack(side="left", padx=10)
        
        self.boton_editar = self.tema.crear_boton_primario(button_frame, "✏️ EDITAR ADMIN", self.editar_admin, 200)
        self.boton_editar.pack(side="left", padx=10)
        
        self.boton_eliminar = self.tema.crear_boton_secundario(button_frame, "🗑️ ELIMINAR ADMIN", self.eliminar_admin, 200)
        self.boton_eliminar.pack(side="left", padx=10)
        
        self.boton_reactivar = self.tema.crear_boton_primario(button_frame, "🔄 REACTIVAR ADMIN", self.reactivar_admin, 200)
        self.boton_reactivar.pack(side="left", padx=10)
        
        self.boton_actualizar = self.tema.crear_boton_primario(button_frame, "🔄 ACTUALIZAR LISTA", self.actualizar_lista, 200)
        self.boton_actualizar.pack(side="right", padx=10)
    
    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            administradores = self.administrador.obtener_todos()
            for admin in administradores:
                estado = "Activo" if admin.get("activo", 1) else "Inactivo"
                self.tree.insert("", "end", values=(
                    admin["id_administrador"],
                    admin["nombre"],
                    admin["telefono"],  # Ahora mostrará el teléfono correctamente
                    admin["correo"],
                    estado
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar administradores: {str(e)}")
    
    def agregar_admin(self):
        nombre = self.nombre_entry.get()
        telefono = self.telefono_entry.get()
        correo = self.correo_entry.get()
        contrasena = self.contrasena_entry.get()
        
        if not nombre or not telefono or not correo or not contrasena:
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
    
    def editar_admin(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un administrador")
            return
        
        item = seleccionado[0]
        valores = self.tree.item(item, "values")
        
        ventana_editar = ctk.CTkToplevel(self.ventana)
        ventana_editar.title("Editar Administrador")
        ventana_editar.geometry("400x500")
        ventana_editar.resizable(False, False)
        ventana_editar.grab_set()
        self.centrar_ventana_secundaria(ventana_editar, "400x500")
        
        titulo = self.tema.crear_subtitulo(ventana_editar, "Editar Administrador")
        titulo.pack(pady=20)
        
        nombre_entry = self.tema.crear_entrada(ventana_editar, "Nombre", 300)
        nombre_entry.insert(0, valores[1])
        nombre_entry.pack(pady=10)
        
        telefono_entry = self.tema.crear_entrada(ventana_editar, "Teléfono", 300)
        telefono_entry.insert(0, valores[2])  # Mostrar el teléfono actual
        telefono_entry.pack(pady=10)
        
        correo_entry = self.tema.crear_entrada(ventana_editar, "Correo", 300)
        correo_entry.insert(0, valores[3])
        correo_entry.configure(state="disabled")
        correo_entry.pack(pady=10)
        
        contrasena_entry = self.tema.crear_entrada(ventana_editar, "Nueva contraseña (dejar vacío para no cambiar)", 300)
        contrasena_entry.configure(show="•")
        contrasena_entry.pack(pady=10)
        
        def guardar_cambios():
            nuevo_nombre = nombre_entry.get()
            nuevo_telefono = telefono_entry.get()
            nueva_contrasena = contrasena_entry.get()
            
            if not nuevo_nombre or not nuevo_telefono:
                messagebox.showerror("Error", "Nombre y teléfono son obligatorios")
                return
            
            if not Validaciones.validar_telefono(nuevo_telefono):
                messagebox.showerror("Error", "Teléfono debe tener al menos 10 dígitos")
                return
            
            try:
                self.administrador.actualizar(valores[0], nuevo_nombre, nuevo_telefono, nueva_contrasena)
                self.actualizar_lista()
                ventana_editar.destroy()
                messagebox.showinfo("Éxito", "Administrador actualizado correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        boton_guardar = self.tema.crear_boton_primario(ventana_editar, "💾 GUARDAR", guardar_cambios, 200)
        boton_guardar.pack(pady=15)
    
    def eliminar_admin(self):
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
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al administrador: {valores[1]}?"):
            try:
                self.administrador.eliminar(id_admin)
                self.actualizar_lista()
                messagebox.showinfo("Éxito", "Administrador eliminado correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def reactivar_admin(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un administrador")
            return
        
        item = seleccionado[0]
        valores = self.tree.item(item, "values")
        
        if valores[4] == "Activo":
            messagebox.showwarning("Advertencia", "Este administrador ya está activo")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de reactivar al administrador: {valores[1]}?"):
            try:
                self.administrador.reactivar(valores[0])
                self.actualizar_lista()
                messagebox.showinfo("Éxito", "Administrador reactivado correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def limpiar_campos(self):
        self.nombre_entry.delete(0, "end")
        self.telefono_entry.delete(0, "end")
        self.correo_entry.delete(0, "end")
        self.contrasena_entry.delete(0, "end")
    
    def centrar_ventana_secundaria(self, ventana, tamanio):
        ventana.update_idletasks()
        ancho = int(tamanio.split('x')[0])
        alto = int(tamanio.split('x')[1])
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"{tamanio}+{x}+{y}")
    
    def volver_principal(self):
        self.ventana.attributes('-fullscreen', False)
        self.ventana.destroy()
        self.ventana_principal.deiconify()