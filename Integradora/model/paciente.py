from base_datos.consultas import ConsultasDB

class Paciente:
    def __init__(self):
        self.consultas = ConsultasDB()
    
    def obtener_todos(self, id_admin):
        return self.consultas.obtener_pacientes(id_admin)
    
    def obtener_con_citas(self, id_admin):
        return self.consultas.obtener_pacientes_con_citas(id_admin)
    
    def crear(self, nombre, dieta, peso, id_admin):
        return self.consultas.agregar_paciente(nombre, dieta, peso, id_admin)
    
    def actualizar(self, id_paciente, nombre, dieta, peso):
        return self.consultas.actualizar_paciente(id_paciente, nombre, dieta, peso)
    
    def eliminar(self, id_paciente):
        try:
            self.consultas.eliminar_citas_por_paciente(id_paciente)
        except Exception as e:
            # Si falla la eliminación de citas, continuamos con el soft delete del paciente
            pass
        
        return self.consultas.eliminar_paciente(id_paciente)