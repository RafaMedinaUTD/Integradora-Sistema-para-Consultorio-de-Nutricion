from base_datos.conexion import ConexionDB

class ConsultasDB:
    def __init__(self):
        self.db = ConexionDB()
    
    def verificar_administrador(self, correo, contrasena):
        query = "SELECT * FROM administrador WHERE correo = %s AND contrasena = %s"
        return self.db.ejecutar_consulta(query, (correo, contrasena))
    
    def registrar_administrador(self, nombre, telefono, correo, contrasena):
        query = "INSERT INTO administrador (nombre, telefono, correo, contrasena) VALUES (%s, %s, %s, %s)"
        return self.db.ejecutar_actualizacion(query, (nombre, telefono, correo, contrasena))
    
    def verificar_correo_existente(self, correo):
        query = "SELECT * FROM administrador WHERE correo = %s"
        return self.db.ejecutar_consulta(query, (correo,))
    
    def obtener_pacientes(self, id_admin):
        query = "SELECT * FROM pacientes WHERE id_admin = %s AND activo = TRUE"
        return self.db.ejecutar_consulta(query, (id_admin,))
    
    def agregar_paciente(self, nombre, dieta, peso, id_admin):
        query = "INSERT INTO pacientes (nombre, dieta, peso, id_admin, activo) VALUES (%s, %s, %s, %s, TRUE)"
        return self.db.ejecutar_actualizacion(query, (nombre, dieta, peso, id_admin))
    
    def actualizar_paciente(self, id_paciente, nombre, dieta, peso):
        query = "UPDATE pacientes SET nombre = %s, dieta = %s, peso = %s WHERE id_paciente = %s"
        return self.db.ejecutar_actualizacion(query, (nombre, dieta, peso, id_paciente))
    
    def eliminar_paciente(self, id_paciente):
        query = "UPDATE pacientes SET activo = FALSE WHERE id_paciente = %s"
        return self.db.ejecutar_actualizacion(query, (id_paciente,))
    
    def obtener_citas(self, id_admin):
        query = """
        SELECT c.id_cita, p.nombre, p.peso, h.dia_semana, 
               TIME_FORMAT(h.hora_inicio, '%H:%i') as hora_inicio,
               TIME_FORMAT(h.hora_fin, '%H:%i') as hora_fin,
               c.fecha, h.id_horario
        FROM citas c 
        JOIN pacientes p ON c.id_paciente = p.id_paciente
        JOIN horarios_disponibles h ON c.id_horario = h.id_horario
        WHERE p.id_admin = %s AND p.activo = TRUE
        """
        return self.db.ejecutar_consulta(query, (id_admin,))
    
    def agregar_cita(self, id_paciente, id_horario, fecha):
        query = "INSERT INTO citas (id_paciente, id_horario, fecha) VALUES (%s, %s, %s)"
        return self.db.ejecutar_actualizacion(query, (id_paciente, id_horario, fecha))
    
    def actualizar_cita(self, id_cita, id_paciente, id_horario, fecha):
        query = "UPDATE citas SET id_paciente = %s, id_horario = %s, fecha = %s WHERE id_cita = %s"
        return self.db.ejecutar_actualizacion(query, (id_paciente, id_horario, fecha, id_cita))
    
    def eliminar_cita(self, id_cita):
        query = "DELETE FROM citas WHERE id_cita = %s"
        return self.db.ejecutar_actualizacion(query, (id_cita,))
    
    def obtener_horarios_disponibles(self):
        query = """
        SELECT id_horario, dia_semana, 
               TIME_FORMAT(hora_inicio, '%H:%i') as hora_inicio,
               TIME_FORMAT(hora_fin, '%H:%i') as hora_fin
        FROM horarios_disponibles 
        ORDER BY 
            FIELD(dia_semana, 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'),
            hora_inicio
        """
        return self.db.ejecutar_consulta(query)
    
    def obtener_horarios_disponibles_por_fecha(self, fecha):
        # Obtener el día de la semana de la fecha
        dia_semana_map = {
            0: 'Lunes',
            1: 'Martes', 
            2: 'Miércoles',
            3: 'Jueves',
            4: 'Viernes',
            5: 'Sábado',
            6: 'Domingo'
        }
        
        from datetime import datetime
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
        dia_semana = dia_semana_map[fecha_obj.weekday()]
        
        query = """
        SELECT h.id_horario, h.dia_semana,
               TIME_FORMAT(h.hora_inicio, '%H:%i') as hora_inicio,
               TIME_FORMAT(h.hora_fin, '%H:%i') as hora_fin
        FROM horarios_disponibles h
        WHERE h.dia_semana = %s 
          AND h.id_horario NOT IN (
              SELECT id_horario FROM citas WHERE fecha = %s
          )
        ORDER BY h.hora_inicio
        """
        return self.db.ejecutar_consulta(query, (dia_semana, fecha))
    
    def generar_horarios_intervalo(self, hora_inicio, hora_fin, intervalo=10):
        """Genera horarios en intervalos específicos"""
        from datetime import datetime, timedelta
        
        horarios = []
        inicio = datetime.strptime(hora_inicio, '%H:%M')
        fin = datetime.strptime(hora_fin, '%H:%M')
        
        while inicio < fin:
            horarios.append(inicio.strftime('%H:%M'))
            inicio += timedelta(minutes=intervalo)
        
        return horarios
    
    def eliminar_citas_por_paciente(self, id_paciente):
        """Elimina todas las citas de un paciente antes de eliminarlo"""
        query = "DELETE FROM citas WHERE id_paciente = %s"
        return self.db.ejecutar_actualizacion(query, (id_paciente,))
    
    def obtener_pacientes_con_citas(self, id_admin):
        """Obtiene pacientes incluyendo información de sus citas"""
        query = """
        SELECT p.*, COUNT(c.id_cita) as total_citas
        FROM pacientes p 
        LEFT JOIN citas c ON p.id_paciente = c.id_paciente
        WHERE p.id_admin = %s AND p.activo = TRUE
        GROUP BY p.id_paciente
        """
        return self.db.ejecutar_consulta(query, (id_admin,))    