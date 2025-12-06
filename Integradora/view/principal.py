import customtkinter as ctk
from tkinter import messagebox
from view.tema import Tema
from view.pacientes import VentanaPacientes
from view.citas import VentanaCitas
from view.admins import VentanaAdmins
from view.ingresos import VentanaIngresos
from configuracion import Configuracion
from model.administrador import Administrador

class VentanaPrincipal:
    def __init__(self, ventana_login, correo_admin, id_admin):
        self.ventana_login = ventana_login
        self.correo_admin = correo_admin
        self.id_admin = id_admin
        self.tema = Tema()
        self.administrador = Administrador()
        
        self.root = ctk.CTkToplevel(ventana_login)
        self.root.title("Sistema Nutriólogo - Principal")
        
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        self.root.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
        self.root.attributes('-fullscreen', True)
        
        self.root.configure(fg_color=self.tema.colores["blanco"])
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_sesion)
        
        # Configurar atajo de teclado para salir de pantalla completa (Esc)
        self.root.bind('<Escape>', lambda e: self.cerrar_sesion())
        
        self.ventana_pacientes = None
        self.ventana_citas = None
        self.ventana_admins = None
        self.ventana_ingresos = None
        
        self.configurar_interfaz()
        self.root.focus_set()
    
    def configurar_interfaz(self):
        # Header más grande para pantalla completa
        header_frame = ctk.CTkFrame(self.root, fg_color=self.tema.colores["verde"], height=140)
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        titulo = ctk.CTkLabel(
            header_frame,
            text="🍎 Sistema Nutriólogo - Panel Principal",
            font=("Roboto", 32, "bold"),
            text_color=self.tema.colores["blanco"]
        )
        titulo.pack(pady=30)
        
        nombre_admin = self.administrador.obtener_nombre_administrador(self.correo_admin)
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(side="right", padx=30)
        
        usuario_label = ctk.CTkLabel(
            info_frame,
            text=f"Bienvenido: {nombre_admin}",
            font=("Roboto Medium", 16),
            text_color=self.tema.colores["blanco"]
        )
        usuario_label.pack()
        
        # Frame principal más grande
        main_frame = ctk.CTkFrame(self.root, fg_color=self.tema.colores["blanco"], border_color=self.tema.colores["gris_claro"], border_width=2, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        botones_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        botones_frame.pack(expand=True)
        
        # Botones más grandes para pantalla completa
        self.titulo_principal = self.tema.crear_titulo(botones_frame, "Acciones")
        self.titulo_principal.pack(pady=(0,20))

        self.boton_pacientes = self.tema.crear_boton_primario(
            botones_frame, 
            "👥 GESTIONAR PACIENTES", 
            self.abrir_pacientes,
            400
        )
        self.boton_pacientes.pack(pady=15)
        
        self.boton_citas = self.tema.crear_boton_primario(
            botones_frame, 
            "📅 GESTIONAR CITAS", 
            self.abrir_citas,
            400
        )
        self.boton_citas.pack(pady=15)
        
        self.boton_ingresos = self.tema.crear_boton_primario(
            botones_frame, 
            "💰 CONTROL DE INGRESOS", 
            self.abrir_ingresos,
            400
        )
        self.boton_ingresos.pack(pady=15)
        
        self.boton_admins = self.tema.crear_boton_primario(
            botones_frame, 
            "👤 GESTIONAR ADMINISTRADORES", 
            self.abrir_admins,
            400
        )
        self.boton_admins.pack(pady=15)
        
        self.boton_salir = self.tema.crear_boton_secundario(
            botones_frame,
            "🚪 CERRAR SESIÓN",
            self.cerrar_sesion,
            400
        )
        self.boton_salir.pack(pady=20)
    
    def abrir_pacientes(self):
        self.root.withdraw() 
        self.ventana_pacientes = VentanaPacientes(self.root, self.id_admin)
    
    def abrir_citas(self):
        self.root.withdraw()  
        self.ventana_citas = VentanaCitas(self.root, self.id_admin)
    
    def abrir_admins(self):
        self.root.withdraw()  
        self.ventana_admins = VentanaAdmins(self.root, self.id_admin)
    
    def abrir_ingresos(self):
        self.root.withdraw()  
        self.ventana_ingresos = VentanaIngresos(self.root, self.id_admin)
    
    def cerrar_sesion(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea cerrar sesión?"):
            self.root.attributes('-fullscreen', False)
            self.root.destroy()
            self.ventana_login.deiconify()