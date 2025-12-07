# Modulo encargado de controlar la interfaz de citas.

import customtkinter as ctk
from tkinter import ttk, messagebox
from model.cita import Cita
from model.paciente import Paciente
from view.tema import Tema
from controller.validaciones import Validaciones

class VistaCitas(ctk.CTkFrame):
    def __init__(self, parent, id_admin):
        super().__init__(parent)
        self.id_admin = id_admin
        self.cita = Cita()
        self.paciente_model = Paciente()
        self.tema = Tema()
        
        self.configure(fg_color=self.tema.colores["blanco"])
        self.configurar_interfaz()
        self.actualizar_lista()
    
    def configurar_interfaz(self): # Metodo encargado de configurar la interfaz.
        # Título de la sección
        titulo = ctk.CTkLabel(self, text="Gestión de Citas", font=("Arial", 28, "bold"), text_color=self.tema.colores["verde"])
        titulo.pack(pady=20)
        
        # --- Campos de entrada para Formulario ---

        # Frame De Formulario
        form_frame = ctk.CTkFrame(self)
        self.tema.aplicar_tema_frame(form_frame)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        self.texto_paciente = self.tema.crear_texto_pequeno(form_frame, "Paciente:")
        self.texto_paciente.pack(side="left", padx=10)
        self.paciente_combobox = ctk.CTkComboBox(form_frame, 
                                                 values=self.obtener_nombres_pacientes(), 
                                                 width=200, 
                                                 dropdown_fg_color="white", 
                                                 dropdown_text_color="black", 
                                                 button_color=self.tema.colores["gris_claro"],
                                                 button_hover_color=self.tema.colores["gris_contraste"],
                                                 border_color=self.tema.colores["gris_claro"])
        self.paciente_combobox.pack(side="left", padx=10, pady=15)
        
        # Fecha
        self.texto_fecha = self.tema.crear_texto_pequeno(form_frame, "Fecha (YYYY-MM-DD):")
        self.texto_fecha.pack(side="left", padx=10)
        self.fecha_entry = self.tema.crear_entrada(form_frame, "YYYY-MM-DD", 120)
        self.fecha_entry.pack(side="left", padx=10, pady=15)
        self.fecha_entry.bind('<KeyRelease>', self.actualizar_horarios_disponibles)
        
        # Horario
        self.texto_horario = self.tema.crear_texto_pequeno(form_frame, "Hora:")
        self.texto_horario.pack(side="left", padx=10)
        self.horario_combobox = ctk.CTkComboBox(form_frame, 
                                                values=[], 
                                                width=100, 
                                                state="disabled", 
                                                dropdown_fg_color="white", 
                                                dropdown_text_color="black", 
                                                button_color=self.tema.colores["gris_claro"],
                                                button_hover_color=self.tema.colores["gris_contraste"],
                                                border_color=self.tema.colores["gris_claro"])
        self.horario_combobox.pack(side="left", padx=10, pady=15)
        
        # Boton Agregar
        self.boton_agregar = self.tema.crear_boton_primario(form_frame, "➕ Agendar", self.agregar_cita, 150)
        self.boton_agregar.pack(side="left", padx=20, pady=15)
        
        # --- Tabla de Citas ---

        # Vista de citas en lista
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Paciente", "Peso", "Día", "Hora", "Fecha"), show="headings", height=15)
        self.tree.tag_configure("impar", background=self.tema.colores["gris_claro"]) #NUEVO 
        self.tree.tag_configure("par", background=self.tema.colores["blanco"]) #NUEVO 

        self.tree.heading("ID", text="ID")
        self.tree.heading("Paciente", text="Paciente")
        self.tree.heading("Peso", text="Peso")
        self.tree.heading("Día", text="Día")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Fecha", text="Fecha")
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Paciente", width=200, anchor="center")
        self.tree.column("Peso", width=60, anchor="center")
        self.tree.column("Día", width=80, anchor="center")
        self.tree.column("Hora", width=80, anchor="center")
        self.tree.column("Fecha", width=100, anchor="center")
        
        # Scrollbar para lista
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- Botones de Acción ---

        # Frame para botones
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=15)
        
        # Boton Editar
        self.boton_editar = self.tema.crear_boton_primario(button_frame, "✏️ Editar", self.editar_cita, 150)
        self.boton_editar.pack(side="left", padx=10)
        
        # Boton Eliminar
        self.boton_eliminar = self.tema.crear_boton_secundario(button_frame, "🗑️ Cancelar Cita", self.eliminar_cita, 150)
        self.boton_eliminar.pack(side="left", padx=10)
        
        # Boton Actualizar
        self.boton_actualizar = self.tema.crear_boton_primario(button_frame, "🔄 Recargar", self.actualizar_lista, 150)
        self.boton_actualizar.pack(side="right", padx=10)

    def obtener_nombres_pacientes(self): # Metodo encargado de obtener la lista de nombres de los pacientes dentro de la interfaz.
        try:
            return [f"{p['id_paciente']} - {p['nombre']} ({p['peso']} kg)" for p in self.paciente_model.obtener_todos(self.id_admin)]
        except: return []

    def actualizar_horarios_disponibles(self, event=None): # Metodo encargado de actualizar horarios disponibles dentro de la interfaz.
        fecha = self.fecha_entry.get()
        if Validaciones.validar_fecha(fecha):
            try:
                horarios = self.cita.obtener_horarios_disponibles_por_fecha(fecha)
                if horarios:
                    opciones = [h['hora'] for h in horarios]
                    self.horario_combobox.configure(values=opciones, state="normal")
                    self.horario_combobox.set(opciones[0] if opciones else "")
                else:
                    self.horario_combobox.configure(values=[], state="disabled")
                    self.horario_combobox.set("")
            except: pass
        else:
            self.horario_combobox.configure(values=[], state="disabled")

    def actualizar_lista(self): # Metodo encargado de actualizar la lista de citas dentro de la interfaz.
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            citas = self.cita.obtener_todas(self.id_admin)
            for i, cita in enumerate(citas):
                tag = "impar" if i % 2 != 0 else "par"
                
                self.tree.insert("", "end", values=(
                    cita["id_cita"],
                    cita["nombre"],
                    cita["peso"],
                    cita["dia_semana"],
                    cita["hora_cita"],
                    cita["fecha"]
                ), tags=(tag,))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def agregar_cita(self): # Metodo encargado de agregar citas dentro de la interfaz.
        
        paciente_txt = self.paciente_combobox.get()
        fecha = self.fecha_entry.get()
        hora = self.horario_combobox.get()
        if not paciente_txt or not fecha or not hora:
            messagebox.showerror("Error", "Campos incompletos")
            return
        if not Validaciones.validar_fecha(fecha):
            messagebox.showerror("Error", "Fecha inválida")
            return
        try:
            id_paciente = paciente_txt.split(" - ")[0]
            horarios = self.cita.obtener_horarios_disponibles_por_fecha(fecha)
            id_horario = next((h['id_horario'] for h in horarios if h['hora'] == hora), None)
            
            if id_horario:
                self.cita.crear(id_paciente, id_horario, fecha, hora)
                self.actualizar_lista()
                self.horario_combobox.set("")
                messagebox.showinfo("Éxito", "Cita agendada")
            else:
                messagebox.showerror("Error", "Horario no válido")
        except Exception as e: messagebox.showerror("Error", str(e))

    def eliminar_cita(self): # Metodo encargado de eliminar citas dentro de la interfaz.
        sel = self.tree.selection()
        if not sel: return
        item = sel[0]
        val = self.tree.item(item, "values")
        if messagebox.askyesno("Confirmar", f"¿Cancelar cita de {val[1]}?"):
            try:
                self.cita.eliminar(val[0])
                self.actualizar_lista()
            except Exception as e: messagebox.showerror("Error", str(e))

    def editar_cita(self): # Metodo encargado de editar citas dentro de la interfaz.
        
        sel = self.tree.selection()
        if not sel: return messagebox.showerror("Error", "Seleccione una cita")
        val = self.tree.item(sel[0], "values")
        id_cita = val[0]
        
        # Ventana emergente para editar
        popup = ctk.CTkToplevel(self)
        popup.title("Editar Cita")
        popup.after(200, lambda: popup.iconbitmap("apple.ico"))
        popup.geometry("400x400")
        popup.grab_set()
        popup.configure(fg_color=self.tema.colores["blanco"])
        self.tema.crear_subtitulo(popup, f"Editando cita de {val[1]}").pack(pady=20)
        
        pacientes = self.paciente_model.obtener_todos(self.id_admin)
        id_paciente_actual = next((p['id_paciente'] for p in pacientes if p['nombre'] == val[1]), None)

        # Fecha
        f_entry = self.tema.crear_entrada(popup, "Fecha", 300)
        f_entry.insert(0, val[5])
        f_entry.pack(pady=10)
        
        h_combo = ctk.CTkComboBox(popup, values=[], width=300, dropdown_fg_color="white", dropdown_text_color="black", 
                                                 button_color=self.tema.colores["gris_claro"],
                                                 button_hover_color=self.tema.colores["gris_contraste"],
                                                 border_color=self.tema.colores["gris_claro"])
        h_combo.pack(pady=10)
        
        def act_horas(e=None): # Metodo encargado de actualizar las horas.
            f = f_entry.get()
            if Validaciones.validar_fecha(f):
                h = [x['hora'] for x in self.cita.obtener_horarios_disponibles_por_fecha(f)]
                h_combo.configure(values=h)
                if val[4] in h: h_combo.set(val[4]) # Mantener hora original si posible
        
        f_entry.bind('<KeyRelease>', act_horas)
        act_horas()
        
        def guardar():
            nf, nh = f_entry.get(), h_combo.get()
            if not nh: return messagebox.showerror("Error", "Seleccione hora")
            try:
                # Buscar ID horario
                hs = self.cita.obtener_horarios_disponibles_por_fecha(nf)
                idh = next((x['id_horario'] for x in hs if x['hora'] == nh), None)
                if idh:
                    self.cita.actualizar(id_cita, id_paciente_actual, idh, nf, nh)
                    self.actualizar_lista()
                    popup.destroy()
                    messagebox.showinfo("Éxito", "Cita reprogramada")
            except Exception as e: messagebox.showerror("Error", str(e))

        self.tema.crear_boton_primario(popup, "Guardar Cambios", guardar, 200).pack(pady=20)