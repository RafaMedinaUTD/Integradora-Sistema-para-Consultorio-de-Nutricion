import customtkinter as ctk
from view.login import LoginApp

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = LoginApp()
    app.run()