"""
NustriSystem v.0.6

Changelog:

    - Agregado un Changelog.
    - Agregados comentarios a todos los modulos para la facilidad de navegacion.
    - Eliminado el modulo "registro.py" remplazado por "admins.py".
    - Version de la aplicacion mostrada en la parte superior de la ventana principal.

"""

import customtkinter as ctk
from view.login import LoginApp
import ctypes

if __name__ == "__main__":
    try:
        myappid = 'nutrisystem.app.nutriologo' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    ctk.set_appearance_mode("light")
    app = LoginApp()
    app.run()