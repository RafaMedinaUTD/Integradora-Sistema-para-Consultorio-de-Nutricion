import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import tkinter as tk
from model.cita import Cita
from model.paciente import Paciente
from view.tema import Tema
from configuracion import Configuracion
from controller.validaciones import Validaciones

class VentanaCitas:
    def __init__(self, ventana_principal, id_admin):
        self.ventana_principal = ventana_principal
        self.id_admin = id_admin
        self.cita = Cita()
        self.paciente_model = Paciente()
        self.tema = Tema()
        
        self.ventana = ctk.CTkToplevel(ventana_principal)
        self.ventana.title("Gestión de Citas")
        
        # Configurar pantalla completa
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        self.ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
        self.ventana.attributes('-fullscreen', True)
        
        self.ventana.configure(fg_color=self.tema.colores["blanco"])
        self.ventana.protocol("WM_DELETE_WINDOW", self.volver_principal)
        
        # Configurar atajo de teclado para salir de pantalla completa (Esc)
        self.ventana.bind('<Escape>', lambda e: self.volver_principal())
        
        self.configurar_interfaz()
        self.actualizar_lista()
        self.ventana.focus_set()
    
    def configurar_interfaz(self):
        header_frame = ctk.CTkFrame(self.ventana, fg_color=self.tema.colores["verde"], height=100)
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        titulo = ctk.CTkLabel(
            header_frame,
            text="Gestión de Citas",
            font=("Arial", 28, "bold"),
            text_color=self.tema.colores["blanco"]
        )
        titulo.pack(pady=25)
        
        form_frame = ctk.CTkFrame(self.ventana)
        self.tema.aplicar_tema_frame(form_frame)
        form_frame.pack(fill="x", padx=20, pady=15)
        
        self.texto_paciente = self.tema.crear_texto_pequeno(form_frame, "Nombre del paciente:")
        self.texto_paciente.pack(side="left", padx=15)
        self.paciente_combobox = ctk.CTkComboBox(
            form_frame,
            values=self.obtener_nombres_pacientes(),
            width=300,
            height=40,
            dropdown_fg_color=self.tema.colores["blanco"],
            dropdown_text_color=self.tema.colores["negro"]
        )
        self.paciente_combobox.pack(side="left", padx=15, pady=15)
        
        self.texto_fecha = self.tema.crear_texto_pequeno(form_frame, "Fecha (YYYY-MM-DD):")
        self.texto_fecha.pack(side="left", padx=15)
        self.fecha_entry = self.tema.crear_entrada(form_frame, "YYYY-MM-DD", 200)
        self.fecha_entry.pack(side="left", padx=15, pady=15)
        self.fecha_entry.bind('<KeyRelease>', self.actualizar_horarios_disponibles)
        
        self.texto_horario = self.tema.crear_texto_pequeno(form_frame, "Horario:")
        self.texto_horario.pack(side="left", padx=15)
        self.horario_combobox = ctk.CTkComboBox(
            form_frame,
            values=[],
            width=200,
            height=40,
            dropdown_fg_color=self.tema.colores["blanco"],
            dropdown_text_color=self.tema.colores["negro"],
            state="disabled"
        )
        self.horario_combobox.pack(side="left", padx=15, pady=15)
        
        self.boton_agregar = self.tema.crear_boton_primario(form_frame, "➕ AGREGAR CITA", self.agregar_cita, 180)
        self.boton_agregar.pack(side="left", padx=15, pady=15)
        
        self.tree_frame = ctk.CTkFrame(self.ventana)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Paciente", "Peso", "Día", "Turno", "Fecha"), show="headings", height=20)
        self.tree.heading("ID", text="ID Cita")
        self.tree.heading("Paciente", text="Nombre del Paciente")
        self.tree.heading("Peso", text="Peso (kg)")
        self.tree.heading("Día", text="Día")
        self.tree.heading("Turno", text="Turno")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.column("ID", width=80)
        self.tree.column("Paciente", width=300)
        self.tree.column("Peso", width=100)
        self.tree.column("Día", width=100)
        self.tree.column("Turno", width=150)
        self.tree.column("Fecha", width=120)
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones más grandes
        button_frame = ctk.CTkFrame(self.ventana)
        button_frame.pack(fill="x", padx=20, pady=15)
        
        self.boton_volver = self.tema.crear_boton_primario(button_frame, "← VOLVER AL MENÚ", self.volver_principal, 250)
        self.boton_volver.pack(side="left", padx=10)
        
        self.boton_editar = self.tema.crear_boton_primario(button_frame, "✏️ EDITAR CITA", self.editar_cita, 200)
        self.boton_editar.pack(side="left", padx=10)
        
        self.boton_eliminar = self.tema.crear_boton_secundario(button_frame, "🗑️ ELIMINAR CITA", self.eliminar_cita, 200)
        self.boton_eliminar.pack(side="left", padx=10)
        
        self.boton_actualizar = self.tema.crear_boton_primario(button_frame, "🔄 ACTUALIZAR LISTA", self.actualizar_lista, 200)
        self.boton_actualizar.pack(side="right", padx=10)
    
    def obtener_nombres_pacientes(self):
        try:
            pacientes = self.paciente_model.obtener_todos(self.id_admin)
            return [f"{p['id_paciente']} - {p['nombre']} ({p['peso']} kg)" for p in pacientes]
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pacientes: {str(e)}")
            return []
    
    def actualizar_horarios_disponibles(self, event=None):
        fecha = self.fecha_entry.get()
        
        if Validaciones.validar_fecha(fecha):
            try:
                horarios = self.cita.obtener_horarios_disponibles_por_fecha(fecha)
                if horarios:
                    opciones_horarios = []
                    for horario in horarios:
                        # Generar intervalos de 10 minutos para cada horario disponible
                        intervalos = self.cita.generar_horarios_intervalo(
                            horario['hora_inicio'], 
                            horario['hora_fin']
                        )
                        for intervalo in intervalos:
                            opciones_horarios.append(f"{horario['dia_semana']} - {intervalo}")
                    
                    self.horario_combobox.configure(values=opciones_horarios, state="normal")
                    if opciones_horarios:
                        self.horario_combobox.set(opciones_horarios[0])
                    else:
                        self.horario_combobox.set("")
                        messagebox.showwarning("Advertencia", "No hay horarios disponibles para esta fecha")
                else:
                    self.horario_combobox.configure(values=[], state="disabled")
                    self.horario_combobox.set("")
                    messagebox.showwarning("Advertencia", "No hay horarios disponibles para esta fecha")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar horarios: {str(e)}")
        else:
            self.horario_combobox.configure(values=[], state="disabled")
            self.horario_combobox.set("")
    
    def obtener_id_paciente(self, texto):
        return texto.split(" - ")[0]
    
    def obtener_id_horario_desde_texto(self, texto_horario):
        try:
            partes = texto_horario.split(" - ")
            dia_semana = partes[0]
            hora = partes[1]
            
            # Buscar el horario en la base de datos
            horarios = self.cita.obtener_horarios_disponibles()
            for horario in horarios:
                if (horario['dia_semana'] == dia_semana and 
                    hora >= horario['hora_inicio'] and 
                    hora < horario['hora_fin']):
                    return horario['id_horario']
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener ID del horario: {str(e)}")
        return None
    
    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            citas = self.cita.obtener_todas(self.id_admin)
            for cita in citas:
                horario_texto = f"{cita['hora_inicio']} - {cita['hora_fin']}"
                self.tree.insert("", "end", values=(
                    cita["id_cita"],
                    cita["nombre"],
                    cita["peso"],
                    cita["dia_semana"],
                    horario_texto,
                    cita["fecha"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar citas: {str(e)}")
    
    def agregar_cita(self):
        paciente_texto = self.paciente_combobox.get()
        fecha = self.fecha_entry.get()
        horario_texto = self.horario_combobox.get()
        
        if not paciente_texto or not fecha or not horario_texto:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if not Validaciones.validar_fecha(fecha):
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            return
        
        try:
            id_paciente = self.obtener_id_paciente(paciente_texto)
            id_horario = self.obtener_id_horario_desde_texto(horario_texto)
            
            if id_horario is None:
                messagebox.showerror("Error", "Horario no válido")
                return
            
            self.cita.crear(id_paciente, id_horario, fecha)
            self.actualizar_lista()
            self.fecha_entry.delete(0, "end")
            self.horario_combobox.set("")
            self.horario_combobox.configure(state="disabled")
            messagebox.showinfo("Éxito", "Cita agregada correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def editar_cita(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione una cita")
            return
        
        item = seleccionado[0]
        valores = self.tree.item(item, "values")
        id_cita = valores[0]
        
        ventana_editar = ctk.CTkToplevel(self.ventana)
        ventana_editar.title("Editar Cita")
        ventana_editar.geometry("400x400")
        ventana_editar.resizable(False, False)
        ventana_editar.grab_set()
        self.centrar_ventana_secundaria(ventana_editar, "400x400")
        
        titulo = self.tema.crear_subtitulo(ventana_editar, "Editar Cita")
        titulo.pack(pady=20)
        
        paciente_label = self.tema.crear_texto_pequeno(ventana_editar, f"Paciente: {valores[1]}")
        paciente_label.pack(pady=5)
        
        id_paciente_actual = None
        try:
            pacientes = self.paciente_model.obtener_todos(self.id_admin)
            for paciente in pacientes:
                if paciente['nombre'] == valores[1]:
                    id_paciente_actual = paciente['id_paciente']
                    break
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener información del paciente: {str(e)}")
            return
        
        fecha_entry = self.tema.crear_entrada(ventana_editar, "Fecha (YYYY-MM-DD)", 300)
        fecha_entry.insert(0, valores[5])
        fecha_entry.pack(pady=10)
        
        horario_combobox = ctk.CTkComboBox(
            ventana_editar,
            values=[],
            width=300,
            height=40,
            dropdown_fg_color=self.tema.colores["blanco"],
            dropdown_text_color=self.tema.colores["negro"]
        )
        horario_combobox.pack(pady=10)
        
        def actualizar_horarios_edicion():
            fecha = fecha_entry.get()
            if Validaciones.validar_fecha(fecha):
                try:
                    horarios = self.cita.obtener_horarios_disponibles_por_fecha(fecha)
                    opciones_horarios = []
                    for horario in horarios:
                        intervalos = self.cita.generar_horarios_intervalo(
                            horario['hora_inicio'], 
                            horario['hora_fin']
                        )
                        for intervalo in intervalos:
                            opciones_horarios.append(f"{horario['dia_semana']} - {intervalo}")
                    
                    horario_combobox.configure(values=opciones_horarios)
                    if opciones_horarios:
                        # Intentar mantener el horario original si está disponible
                        horario_original = f"{valores[3]} - {valores[4].split(' - ')[0]}"
                        if horario_original in opciones_horarios:
                            horario_combobox.set(horario_original)
                        else:
                            horario_combobox.set(opciones_horarios[0])
                except Exception as e:
                    messagebox.showerror("Error", f"Error al cargar horarios: {str(e)}")
        
        fecha_entry.bind('<KeyRelease>', lambda e: actualizar_horarios_edicion())
        actualizar_horarios_edicion()
        
        def guardar_cambios():
            nueva_fecha = fecha_entry.get()
            nuevo_horario = horario_combobox.get()
            
            if not Validaciones.validar_fecha(nueva_fecha):
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
                return
            
            if not nuevo_horario:
                messagebox.showerror("Error", "Seleccione un horario")
                return
            
            try:
                id_horario = self.obtener_id_horario_desde_texto(nuevo_horario)
                if id_horario is None:
                    messagebox.showerror("Error", "Horario no válido")
                    return
                
                self.cita.actualizar(id_cita, id_paciente_actual, id_horario, nueva_fecha)
                self.actualizar_lista()
                ventana_editar.destroy()
                messagebox.showinfo("Éxito", "Cita actualizada correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        boton_guardar = self.tema.crear_boton_primario(ventana_editar, "💾 GUARDAR", guardar_cambios, 200)
        boton_guardar.pack(pady=15)
    
    def centrar_ventana_secundaria(self, ventana, tamanio):
        ventana.update_idletasks()
        ancho = int(tamanio.split('x')[0])
        alto = int(tamanio.split('x')[1])
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"{tamanio}+{x}+{y}")
    
    def eliminar_cita(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione una cita")
            return
        
        item = seleccionado[0]
        valores = self.tree.item(item, "values")
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la cita de {valores[1]}?"):
            try:
                self.cita.eliminar(valores[0])
                self.actualizar_lista()
                messagebox.showinfo("Éxito", "Cita eliminada correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def volver_principal(self):
        self.ventana.attributes('-fullscreen', False)
        self.ventana.destroy()
        self.ventana_principal.deiconify()