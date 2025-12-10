import customtkinter as ctk
from tkinter import messagebox
from model.administrador import Administrador
from view.tema import Tema
from configuracion import Configuracion
from controller.validaciones import Validaciones

class VentanaRegistro:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.administrador = Administrador()
        self.tema = Tema()
        
        self.ventana = ctk.CTkToplevel(ventana_principal)
        self.ventana.title("Registro de Administrador")
        self.ventana.geometry(Configuracion.TAMANOS["registro"])
        self.ventana.resizable(False, False)
        self.ventana.configure(fg_color=self.tema.colores["blanco"])
        self.ventana.grab_set()
        self.ventana.protocol("WM_DELETE_WINDOW", self.volver_principal)
        
        # Centrar ventana
        self.centrar_ventana(self.ventana, Configuracion.TAMANOS["registro"])
        
        self.configurar_interfaz()
    
    def centrar_ventana(self, ventana, tamanio):
        ventana.update_idletasks()
        ancho_ventana = int(tamanio.split('x')[0])
        alto_ventana = int(tamanio.split('x')[1])
        x = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        ventana.geometry(f"{tamanio}+{x}+{y}")
    
    def configurar_interfaz(self):
        self.logo_label = ctk.CTkLabel(
            self.ventana,
            text="🍎",
            font=("Arial", 60),
            text_color=self.tema.colores["verde"]
        )
        self.logo_label.pack(pady=20)
        
        self.registro_frame = ctk.CTkFrame(self.ventana)
        self.tema.aplicar_tema_frame(self.registro_frame)
        self.registro_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        self.titulo = self.tema.crear_titulo(self.registro_frame, "REGISTRO DE ADMINISTRADOR")
        self.titulo.pack(pady=20)
        
        self.subtitulo_nombre = self.tema.crear_texto_pequeno(self.registro_frame, "Nombre completo: ")
        self.subtitulo_nombre.pack(pady=0)
        self.nombre_entry = self.tema.crear_entrada(self.registro_frame, "John Doe", 300)
        self.nombre_entry.pack(pady=8)
        
        self.subtitulo_telefono = self.tema.crear_texto_pequeno(self.registro_frame, "Teléfono: ")
        self.subtitulo_telefono.pack(pady=0)
        self.telefono_entry = self.tema.crear_entrada(self.registro_frame, "(xxx) xxx-xxxx", 300)
        self.telefono_entry.pack(pady=8)
        
        self.subtitulo_correo = self.tema.crear_texto_pequeno(self.registro_frame, "Correo electrónico: ")
        self.subtitulo_correo.pack(pady=0)
        self.correo_entry = self.tema.crear_entrada(self.registro_frame, "example@email.com", 300)
        self.correo_entry.pack(pady=8)
        
        self.subtitulo_contrasena = self.tema.crear_texto_pequeno(self.registro_frame, "Contraseña: ")
        self.subtitulo_contrasena.pack(pady=0)
        self.contrasena_entry = self.tema.crear_entrada(self.registro_frame, "******", 300)
        self.contrasena_entry.configure(show="•")
        self.contrasena_entry.pack(pady=8)
        
        self.subtitulo_confirmarcontrasena = self.tema.crear_texto_pequeno(self.registro_frame, "Confirmar contraseña: ")
        self.subtitulo_confirmarcontrasena.pack(pady=0)
        self.confirmar_contrasena_entry = self.tema.crear_entrada(self.registro_frame, "******", 300)
        self.confirmar_contrasena_entry.configure(show="•")
        self.confirmar_contrasena_entry.pack(pady=8)
        
        self.registro_button = self.tema.crear_boton_primario(self.registro_frame, "Registrar Administrador", self.registrar_admin, 300)
        self.registro_button.pack(pady=15)
        
        self.cancelar_button = self.tema.crear_boton_secundario(self.registro_frame, "Volver al Menú", self.volver_principal, 300)
        self.cancelar_button.pack(pady=5)
        
        self.mensaje_label = ctk.CTkLabel(
            self.registro_frame,
            text="",
            text_color=self.tema.colores["rojo"]
        )
        self.mensaje_label.pack(pady=10)
    
    def registrar_admin(self):
        nombre = self.nombre_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        correo = self.correo_entry.get().strip()
        contrasena = self.contrasena_entry.get()
        confirmar_contrasena = self.confirmar_contrasena_entry.get()
        
        if not all([nombre, telefono, correo, contrasena, confirmar_contrasena]):
            self.mostrar_mensaje("Todos los campos son obligatorios")
            return
        
        if not Validaciones.validar_correo(correo):
            self.mostrar_mensaje("El formato del correo no es válido")
            return
        
        if not telefono.isdigit() or len(telefono) < 10:
            self.mostrar_mensaje("El teléfono debe contener solo números y tener al menos 10 dígitos")
            return
        
        if contrasena != confirmar_contrasena:
            self.mostrar_mensaje("Las contraseñas no coinciden")
            return
        
        if len(contrasena) < 6:
            self.mostrar_mensaje("La contraseña debe tener al menos 6 caracteres")
            return
        
        try:
            if self.administrador.verificar_correo_existente(correo):
                self.mostrar_mensaje("El correo ya está registrado")
                return
            
            self.administrador.registrar(nombre, telefono, correo, contrasena)
            messagebox.showinfo("Éxito", "Administrador registrado exitosamente.")
            self.volver_principal()
            
        except Exception as e:
            self.mostrar_mensaje(f"Error en el registro: {str(e)}")
    
    def mostrar_mensaje(self, mensaje):
        self.mensaje_label.configure(text=mensaje, text_color=self.tema.colores["rojo"])
    
    def volver_principal(self):
        self.ventana.destroy()
        self.ventana_principal.deiconify()