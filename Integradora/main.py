"""
NustriSystem v.0.7.1

Changelog:

    - Arreglado un error de layout.

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