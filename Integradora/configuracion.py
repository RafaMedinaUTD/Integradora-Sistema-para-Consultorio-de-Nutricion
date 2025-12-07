# Modulo encargado de controlar la configuracion en diferentes modulos.
# Se uso formato JSON para almacenar las diferentes variables.

class Configuracion:
    
    # Lista con colores usados para la aplicacion.
    COLORES = {
        "verde": "#568B37",
        "verde_hover": "#316E39",
        "blanco": "#FFFFFF",
        "negro": "#000000",
        "rojo": "#BD4941",
        "rojo_claro": "#F3BFBB",
        "rojo_hover": "#9B3A47",
        "gris": "#234128",
        "gris_claro": "#C5D1BD",
        "gris_contraste": "#9EB69B",
    }
    
    # Lista con fuentes usados en los elementos de texto.
    FUENTES = {
        "titulo": ("Helvetica", 24, "bold"),
        "subtitulo": ("Helvetica", 18),
        "normal": ("Helvetica", 14),
        "boton": ("Helvetica Medium", 14),
        "pequeno": ("Helvetica", 11)
    }
    
    # Lista con datos usados para la base de datos.
    BASE_DATOS = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "nutriologo"
    }
    
    # Lista usada para los tamaños de ventana en los diferentes modulos.
    TAMANOS = {
        "login": "500x600",
        "principal": "pantalla_completa",
        "pacientes": "pantalla_completa",
        "citas": "pantalla_completa",
        "admins": "pantalla_completa",
        "ingresos": "pantalla_completa",
        "editar": "400x400"
    }