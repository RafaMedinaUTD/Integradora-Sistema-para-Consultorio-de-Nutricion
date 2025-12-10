# Modulo encargado de controlar la interfaz de login.

import customtkinter as ctk
from model.administrador import Administrador
from view.tema import Tema
from view.principal import VentanaPrincipal
from configuracion import Configuracion
from tkinter import PhotoImage

class LoginApp:
    def __init__(self):
        self.administrador = Administrador()
        self.tema = Tema()
        
        self.root = ctk.CTk()
        self.root.title("NutriSystem - Login")
        self.root.configure(fg_color=self.tema.colores["blanco"])
        

        
        self.restaurar_login()
    
    def restaurar_login(self): # Metodo encargado de restaurar la ventana de Login a su estado original despues de cerrar sesion.
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.centrar_ventana(self.root, Configuracion.TAMANOS["login"])
        self.root.attributes('-fullscreen', False)
        
        self.configurar_interfaz()

    def iniciar_aplicacion_principal(self): # Metodo encargado de iniciar el panel de control.
        """Limpia el login e inicia la Ventana Principal"""
        id_admin = self.administrador.obtener_id_administrador(self.correo_actual)
        
        for widget in self.root.winfo_children():
            widget.destroy()
            
        VentanaPrincipal(self.root, self.correo_actual, id_admin, self.restaurar_login)

    def centrar_ventana(self, ventana, tamanio): # Metodo encargado de centrar la ventana de Login.
        ventana.update_idletasks()
        try:
            ancho = int(tamanio.split('x')[0])
            alto = int(tamanio.split('x')[1])
        except: ancho, alto = 500, 600
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def configurar_interfaz(self): # Metodo encargado de configurar la interfaz.

        # Titulo, Logotipo e Isotipo
        self.logo_label = ctk.CTkLabel(self.root, text="🍎 NutriSystem", font=("Helvetica", 40, "bold"), text_color=self.tema.colores["verde"]).pack(pady=(40, 0))
        self.tema.crear_subtitulo(self.root, "Consultorio Dr. Angel Medina").pack(pady=(10,10))

        # --- Campos de entrada para Formulario ---

        # Frame De Login
        self.login_frame = ctk.CTkFrame(self.root)
        self.tema.aplicar_tema_frame(self.login_frame)
        self.login_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Label Login
        self.tema.crear_titulo(self.login_frame, "INICIAR SESIÓN").pack(pady=20)
        
        # Entrada Correo Electronico
        self.tema.crear_texto_pequeno(self.login_frame, "Correo electrónico: ").pack(pady=0)
        self.correo_entry = self.tema.crear_entrada(self.login_frame, "example@email.com", 300)
        self.correo_entry.pack(pady=12)
        
        # Entrada Contraseña
        self.tema.crear_texto_pequeno(self.login_frame, "Contraseña: ").pack(pady=0)
        self.contrasena_entry = self.tema.crear_entrada(self.login_frame, "******", 300)
        self.contrasena_entry.configure(show="•")
        self.contrasena_entry.pack(pady=12)
        
        # Boton Ingresar
        self.tema.crear_boton_primario(self.login_frame, "Ingresar", self.verificar_login, 300).pack(pady=15)

        # Boton Salir
        self.tema.crear_boton_secundario(self.login_frame, "Salir", self.salir, 300).pack(pady=15)
        
        # Label Aviso
        self.mensaje_label = ctk.CTkLabel(self.login_frame, text="", text_color=self.tema.colores["rojo"])
        self.mensaje_label.pack(pady=10)

    def verificar_login(self): # Metodo encargado de verificar si los datos son correctos.
        correo = self.correo_entry.get()
        contrasena = self.contrasena_entry.get()
        if not correo or not contrasena:
            self.mensaje_label.configure(text="Campos obligatorios")
            return
        try:
            if self.administrador.login(correo, contrasena):
                self.correo_actual = correo
                self.mensaje_label.configure(text="¡Login exitoso!", text_color=self.tema.colores["verde"])
                self.root.after(500, self.iniciar_aplicacion_principal)
            else:
                self.mensaje_label.configure(text="Credenciales incorrectas")
        except Exception as e:
            self.mensaje_label.configure(text=f"Error: {str(e)}")

    def salir(self): # Metodo encargado de salir de la aplicacion.
        self.root.destroy()

    def run(self): # Metodo encargado de arrancar la aplicacion.
        self.root.mainloop()