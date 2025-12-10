# Modulo encargado de controlar la interfaz principal de la aplicacion.

import customtkinter as ctk
from tkinter import messagebox
from view.tema import Tema
from view.pacientes import VistaPacientes
from view.citas import VistaCitas
from view.admins import VistaAdmins
from view.ingresos import VistaIngresos
from model.administrador import Administrador
from tkinter import PhotoImage

class VentanaPrincipal:
    def __init__(self, root, correo_admin, id_admin, logout_callback):
        self.root = root
        self.correo_admin = correo_admin
        self.id_admin = id_admin
        self.logout_callback = logout_callback
        self.tema = Tema()
        self.administrador = Administrador()
        
        self.root.title("NutriSystem - Panel Principal")
        
        
        
        # Configurar pantalla completa
        ancho = self.root.winfo_screenwidth()
        alto = self.root.winfo_screenheight()
        self.root.geometry(f"{ancho}x{alto}+0+0")
        self.root.attributes('-fullscreen', True)
        
        # Atajo Esc para salir
        self.root.bind('<Escape>', lambda e: self.cerrar_sesion())
        
        # Vista por defecto en el contenido: Pacientes
        self.vista_actual = None
        self.configurar_layout()
        self.mostrar_vista("pacientes")

    def configurar_layout(self): # Metodo encargado de configurar el layout.
        # --- Menu Lateral (SIDEBAR) ---
        self.sidebar_frame = ctk.CTkFrame(self.root, width=300, corner_radius=0, fg_color=self.tema.colores["verde"])
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False) # Forzar ancho fijo

        # Titulo, Logotipo e Isotipo
        logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="🍎\nNutriSystem", 
            font=("Helvetica", 24, "bold"),
            text_color=self.tema.colores["blanco"]
        )
        logo_label.pack(pady=(40, 20))

        # Nombre Usuario Activo
        nombre_admin = self.administrador.obtener_nombre_administrador(self.correo_admin)
        primer_nombre = nombre_admin.split(" ")[0] if nombre_admin else "Admin"
        
        # Consultorio
        user_label = ctk.CTkLabel(
            self.sidebar_frame,
            text=f"Consultorio Dr. Angel Medina",
            font=("Helvetica", 16),
            text_color=self.tema.colores["blanco"]
        )
        user_label.pack(pady=(0, 20))

        # Usuario Activo
        active_label = ctk.CTkLabel(
            self.sidebar_frame,
            text=f"Usuario Activo: {primer_nombre}",
            font=("Helvetica", 12),
            text_color=self.tema.colores["blanco"],
            )
        active_label.pack(pady=(0,0))
        
        # --- Botones de Acción ---

        # Botón Pacientes
        self.crear_boton_menu("👥 Pacientes", "pacientes")

        # Botón Citas
        self.crear_boton_menu("📅 Citas", "citas")

        # Botón Ingresos
        self.crear_boton_menu("💰 Ingresos", "ingresos")

        # Botón Administradores
        self.crear_boton_menu("👤 Administradores", "admins")
        
        # Espaciador
        ctk.CTkLabel(self.sidebar_frame, text="").pack(expand=True)

        # Botón Salir
        btn_salir = ctk.CTkButton(
            self.sidebar_frame,
            text="🚪 Cerrar Sesión",
            command=self.cerrar_sesion,
            fg_color=self.tema.colores["rojo"],
            hover_color=self.tema.colores["rojo_hover"],
            text_color=self.tema.colores["blanco"],
            corner_radius=10,
            font=("Helvetica", 14, "bold"),
            height=40,
            anchor="center"
        )
        btn_salir.pack(pady=40, padx=20, fill="x")

        # --- Área de Contenido Principal ---

        # Frame de Contenido Principal
        self.main_content = ctk.CTkFrame(self.root, fg_color=self.tema.colores["blanco"], corner_radius=0)
        self.main_content.pack(side="right", fill="both", expand=True)

    def crear_boton_menu(self, texto, vista_key): # Metodo encargado de crear botones en el sidebar.
        btn = ctk.CTkButton(
            self.sidebar_frame,
            text=texto,
            command=lambda: self.mostrar_vista(vista_key),
            fg_color=self.tema.colores["verde"],
            text_color=self.tema.colores["blanco"],
            hover_color=self.tema.colores["verde_hover"],
            font=("Helvetica", 16, "bold"),
            corner_radius=0,
            height=50,
            anchor="center"
        )
        btn.pack(fill="x", padx=0, pady=20)

    def mostrar_vista(self, vista_key): # Metodo encargado de mostrar el contenido en el layout.
        # Eliminar la vista anterior
        if self.vista_actual:
            self.vista_actual.destroy()
        
        # Crear la nueva vista
        if vista_key == "pacientes":
            self.vista_actual = VistaPacientes(self.main_content, self.id_admin)
        elif vista_key == "citas":
            self.vista_actual = VistaCitas(self.main_content, self.id_admin)
        elif vista_key == "admins":
            self.vista_actual = VistaAdmins(self.main_content, self.id_admin)
        elif vista_key == "ingresos":
            self.vista_actual = VistaIngresos(self.main_content, self.id_admin)
            
        self.vista_actual.pack(fill="both", expand=True, padx=20, pady=20)

    def cerrar_sesion(self): # Metodo encargado de cerrar sesion.
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea cerrar sesión?"):
            if self.logout_callback:
                self.logout_callback()