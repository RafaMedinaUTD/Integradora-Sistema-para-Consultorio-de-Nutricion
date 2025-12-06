import customtkinter as ctk
from configuracion import Configuracion

class Tema:
    def __init__(self):
        self.colores = Configuracion.COLORES
        self.fuentes = Configuracion.FUENTES
    
    def aplicar_tema_frame(self, frame):
        frame.configure(
            fg_color=self.colores["blanco"],
            border_color=self.colores["gris_claro"],
            border_width=2,
            corner_radius=10
        )
    
    def crear_boton_primario(self, parent, texto, comando, width=200):
        return ctk.CTkButton(
            parent,
            text=texto,
            command=comando,
            width=width,
            height=40,
            corner_radius=10,
            fg_color=self.colores["verde"],
            hover_color=self.colores["verde_hover"],
            text_color=self.colores["blanco"],
            font=self.fuentes["boton"]
        )
    
    def crear_boton_secundario(self, parent, texto, comando, width=200):
        return ctk.CTkButton(
            parent,
            text=texto,
            command=comando,
            width=width,
            height=40,
            corner_radius=10,
            fg_color=self.colores["rojo"],
            hover_color=self.colores["rojo_hover"],
            text_color=self.colores["blanco"],
            font=self.fuentes["boton"]
        )
    
    def crear_entrada(self, parent, placeholder, width=250):
        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            width=width,
            height=40,
            border_width=2,
            corner_radius=10,
            border_color=self.colores["gris_claro"],
            fg_color=self.colores["blanco"],
            text_color=self.colores["negro"]
        )
    
    def crear_titulo(self, parent, texto):
        return ctk.CTkLabel(
            parent,
            text=texto,
            font=self.fuentes["titulo"],
            text_color=self.colores["negro"]
        )
    
    def crear_subtitulo(self, parent, texto):
        return ctk.CTkLabel(
            parent,
            text=texto,
            font=self.fuentes["subtitulo"],
            text_color=self.colores["negro"]
        )
    
    def crear_texto_pequeno(self, parent, texto):
        return ctk.CTkLabel(
            parent,
            text=texto,
            font=self.fuentes["pequeno"],
            text_color=self.colores["negro"]
        )