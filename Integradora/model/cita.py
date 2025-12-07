# Modulo encargado de controlar las operaciones dentro de citas.

from base_datos.consultas import ConsultasDB

class Cita:
    def __init__(self):
        self.consultas = ConsultasDB()
    
    def obtener_todas(self, id_admin):
        return self.consultas.obtener_citas(id_admin)
    
    def crear(self, id_paciente, id_horario, fecha, hora_cita):
        return self.consultas.agregar_cita(id_paciente, id_horario, fecha, hora_cita)
    
    def actualizar(self, id_cita, id_paciente, id_horario, fecha, hora_cita):
        return self.consultas.actualizar_cita(id_cita, id_paciente, id_horario, fecha, hora_cita)
    
    def eliminar(self, id_cita):
        return self.consultas.eliminar_cita(id_cita)
    
    def obtener_horarios_disponibles(self):
        return self.consultas.obtener_horarios_disponibles()
    
    def obtener_horarios_disponibles_por_fecha(self, fecha):
        return self.consultas.obtener_horarios_disponibles_por_fecha(fecha)
    
    def generar_horarios_intervalo(self, hora_inicio, hora_fin, intervalo=10):
        return self.consultas.generar_horarios_intervalo(hora_inicio, hora_fin, intervalo)