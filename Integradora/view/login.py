import customtkinter as ctk
from model.administrador import Administrador
from view.tema import Tema
from view.principal import VentanaPrincipal
from configuracion import Configuracion

class LoginApp:
    def __init__(self):
        self.administrador = Administrador()
        self.tema = Tema()
        
        self.root = ctk.CTk()
        self.root.title("Sistema Nutriólogo - Login")
        self.root.geometry(Configuracion.TAMANOS["login"])
        self.root.resizable(False, False)
        self.root.configure(fg_color=self.tema.colores["blanco"])
        
        self.centrar_ventana(self.root, Configuracion.TAMANOS["login"])
        
        self.correo_actual = ""
        self.ventana_principal = None
        self.configurar_interfaz()
    
    def centrar_ventana(self, ventana, tamanio):
        if tamanio == "pantalla_completa":
            ancho = ventana.winfo_screenwidth()
            alto = ventana.winfo_screenheight()
            ventana.geometry(f"{ancho}x{alto}+0+0")
        else:
            ventana.update_idletasks()
            ancho_ventana = int(tamanio.split('x')[0])
            alto_ventana = int(tamanio.split('x')[1])
            x = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
            y = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
            ventana.geometry(f"{tamanio}+{x}+{y}")
    
    def configurar_interfaz(self):
        self.logo_label = ctk.CTkLabel(
            self.root,
            text="🍎",
            font=("Arial", 80),
            text_color=self.tema.colores["verde"]
        )
        self.logo_label.pack(pady=40)
        
        self.login_frame = ctk.CTkFrame(self.root)
        self.tema.aplicar_tema_frame(self.login_frame)
        self.login_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        self.titulo = self.tema.crear_titulo(self.login_frame, "INICIAR SESIÓN")
        self.titulo.pack(pady=20)
        
        self.subtitulo_correo = self.tema.crear_texto_pequeno(self.login_frame, "Correo electrónico: ")
        self.subtitulo_correo.pack(pady=0)
        self.correo_entry = self.tema.crear_entrada(self.login_frame, "example@email.com", 300)
        self.correo_entry.pack(pady=12)
        
        self.subtitulo_contraseña = self.tema.crear_texto_pequeno(self.login_frame, "Contraseña: ")
        self.subtitulo_contraseña.pack(pady=0)
        self.contrasena_entry = self.tema.crear_entrada(self.login_frame, "******", 300)
        self.contrasena_entry.configure(show="•")
        self.contrasena_entry.pack(pady=12)
        
        self.login_button = self.tema.crear_boton_primario(self.login_frame, "Ingresar", self.verificar_login, 300)
        self.login_button.pack(pady=15)
        
        self.mensaje_label = ctk.CTkLabel(
            self.login_frame,
            text="",
            text_color=self.tema.colores["rojo"]
        )
        self.mensaje_label.pack(pady=10)
    
    def verificar_login(self):
        correo = self.correo_entry.get()
        contrasena = self.contrasena_entry.get()

        if not correo or not contrasena:
            self.mostrar_mensaje("Todos los campos son obligatorios")
            return

        try:
            if self.administrador.login(correo, contrasena):
                self.correo_actual = correo
                self.mostrar_mensaje("¡Login exitoso!", True)
                self.root.after(1000, self.abrir_ventana_principal)
            else:
                self.mostrar_mensaje("Credenciales incorrectas")
        except Exception as e:
            self.mostrar_mensaje(f"Error: {str(e)}")
    
    def mostrar_mensaje(self, mensaje, exito=False):
        color = self.tema.colores["verde"] if exito else self.tema.colores["rojo"]
        self.mensaje_label.configure(text=mensaje, text_color=color)
    
    def abrir_ventana_principal(self):
        self.root.withdraw()  
        id_admin = self.administrador.obtener_id_administrador(self.correo_actual)
        self.ventana_principal = VentanaPrincipal(self.root, self.correo_actual, id_admin)
    
    def run(self):
        self.root.mainloop()