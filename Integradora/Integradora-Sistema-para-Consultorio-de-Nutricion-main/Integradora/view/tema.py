# Modulo encargado de controlar los elementos de diferentes interfaces.

import customtkinter as ctk
from tkinter import ttk
from configuracion import Configuracion

class Tema:
    def __init__(self):
        self.colores = Configuracion.COLORES
        self.fuentes = Configuracion.FUENTES
    
    def aplicar_tema_frame(self, frame): # Metodo encargado de configurar las visuales de los frames.
        frame.configure(
            fg_color=self.colores["blanco"],
            border_color=self.colores["gris_claro"],
            border_width=2,
            corner_radius=10
        )
    
    def crear_boton_primario(self, parent, texto, comando, width=200): # Metodo encargado de configurar las visuales de los botones primarios.
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
    
    def crear_boton_secundario(self, parent, texto, comando, width=200): # Metodo encargado de configurar las visuales de los botones secundarios.
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
    
    def crear_entrada(self, parent, placeholder, width=250): # Metodo encargado de configurar las visuales de las entradas de texto.
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
    
    def crear_titulo(self, parent, texto): # Metodo encargado de configurar las visuales de los titulos.
        return ctk.CTkLabel(
            parent,
            text=texto,
            font=self.fuentes["titulo"],
            text_color=self.colores["negro"]
        )
    
    def crear_subtitulo(self, parent, texto): # Metodo encargado de configurar las visuales de los subtitulos.
        return ctk.CTkLabel(
            parent,
            text=texto,
            font=self.fuentes["subtitulo"],
            text_color=self.colores["negro"]
        )
    
    def crear_texto_pequeno(self, parent, texto): # Metodo encargado de configurar las visuales de los textos pequeños.
        return ctk.CTkLabel(
            parent,
            text=texto,
            font=self.fuentes["pequeno"],
            text_color=self.colores["negro"]
        )
    
    def configurar_estilo_tablas(self): # Metodo encargado de configurar las visuales de las tablas de contenido.
        style = ttk.Style()
        
        style.theme_use("clam") 

        style.configure(
            "Treeview",
            background=self.colores["blanco"],
            foreground=self.colores["negro"],
            fieldbackground=self.colores["blanco"],
            borderwidth=0,
            rowheight=35,
            font=("Helvetica", 12)
        )
        
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) 

        style.map(
            "Treeview",
            background=[('selected', self.colores["verde_hover"])],
            foreground=[('selected', self.colores["blanco"])]      
        )

        style.configure(
            "Treeview.Heading",
            background=self.colores["verde"],      
            foreground=self.colores["blanco"],      
            relief="flat",                         
            font=("Helvetica", 12, "bold"),            
            padding=(10, 5)                        
        )
        
        style.map(
            "Treeview.Heading",
            background=[('active', self.colores["verde_hover"])] 
        )