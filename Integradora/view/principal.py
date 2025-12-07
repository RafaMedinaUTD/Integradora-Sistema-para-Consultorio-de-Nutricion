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
    def __init__(self, root, correo_admin, id_admin, logout_callback): # <--- Nuevo parámetro
        self.root = root
        self.correo_admin = correo_admin
        self.id_admin = id_admin
        self.logout_callback = logout_callback # <--- Guardamos la función para usarla luego
        self.tema = Tema()
        self.administrador = Administrador()
        
        self.root.title("NutriSystem - Panel Principal")
        
        # Icono
        # Metodo 1
        self.root.wm_iconbitmap("apple.ico")
        # Metodo 2
        icon_img = PhotoImage(file="apple.png")
        self.root.iconphoto(False, icon_img)
        
        # Configurar pantalla completa
        ancho = self.root.winfo_screenwidth()
        alto = self.root.winfo_screenheight()
        self.root.geometry(f"{ancho}x{alto}+0+0")
        self.root.attributes('-fullscreen', True)
        
        # Atajo Esc para salir
        self.root.bind('<Escape>', lambda e: self.cerrar_sesion())
        
        self.vista_actual = None
        self.configurar_layout()
        self.mostrar_vista("pacientes")

    def configurar_layout(self):
        # --- MENÚ LATERAL (SIDEBAR) ---
        self.sidebar_frame = ctk.CTkFrame(self.root, width=300, corner_radius=0, fg_color=self.tema.colores["verde"])
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False) # Forzar ancho fijo

        # Logo / Título Sidebar
        logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="🍎\nNutriSystem", 
            font=("Helvetica", 24, "bold"),
            text_color=self.tema.colores["blanco"]
        )
        logo_label.pack(pady=(40, 20))

        # Info Usuario
        nombre_admin = self.administrador.obtener_nombre_administrador(self.correo_admin)
        # Tomar solo el primer nombre para que quepa bien
        primer_nombre = nombre_admin.split(" ")[0] if nombre_admin else "Admin"
        
        user_label = ctk.CTkLabel(
            self.sidebar_frame,
            text=f"Consultorio Dr. Angel Medina",
            font=("Helvetica", 16),
            text_color=self.tema.colores["blanco"]
        )
        user_label.pack(pady=(0, 30))

        self.tema.crear_texto_pequeno(self.root, f"Usuario: {primer_nombre}").pack(pady=(10,0))
        
        # Botones de Navegación
        self.crear_boton_menu("👥 Pacientes", "pacientes")
        self.crear_boton_menu("📅 Citas", "citas")
        self.crear_boton_menu("💰 Ingresos", "ingresos")
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

        # --- ÁREA DE CONTENIDO PRINCIPAL ---
        self.main_content = ctk.CTkFrame(self.root, fg_color=self.tema.colores["blanco"], corner_radius=0)
        self.main_content.pack(side="right", fill="both", expand=True)

    def crear_boton_menu(self, texto, vista_key):
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

    def mostrar_vista(self, vista_key):
        # Eliminar la vista anterior
        if self.vista_actual:
            self.vista_actual.destroy()
        
        # Crear la nueva vista dentro del main_content
        if vista_key == "pacientes":
            self.vista_actual = VistaPacientes(self.main_content, self.id_admin)
        elif vista_key == "citas":
            self.vista_actual = VistaCitas(self.main_content, self.id_admin)
        elif vista_key == "admins":
            self.vista_actual = VistaAdmins(self.main_content, self.id_admin)
        elif vista_key == "ingresos":
            self.vista_actual = VistaIngresos(self.main_content, self.id_admin)
            
        # Empaquetar la vista para que ocupe todo el espacio
        self.vista_actual.pack(fill="both", expand=True, padx=20, pady=20)

    def cerrar_sesion(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea cerrar sesión?"):
            if self.logout_callback:
                self.logout_callback()