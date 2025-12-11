# Integradora/base_datos/consultas.py

from base_datos.conexion import ConexionDB
from datetime import datetime

class ConsultasDB:
    def __init__(self):
        self.db = ConexionDB()
    
    # --- Consultas para administradores ---

    def verificar_administrador(self, correo, contrasena):
        query = "SELECT * FROM administrador WHERE correo = ? AND contrasena = ? AND activo = 1"
        return self.db.ejecutar_consulta(query, (correo, contrasena))
    
    def registrar_administrador(self, nombre, telefono, correo, contrasena):
        query = "INSERT INTO administrador (nombre, telefono, correo, contrasena, activo) VALUES (?, ?, ?, ?, 1)"
        return self.db.ejecutar_actualizacion(query, (nombre, telefono, correo, contrasena))
    
    def verificar_correo_existente(self, correo):
        query = "SELECT * FROM administrador WHERE correo = ?"
        return self.db.ejecutar_consulta(query, (correo,))
    
    def obtener_administradores(self):
        query = "SELECT * FROM administrador ORDER BY activo DESC, nombre ASC"
        return self.db.ejecutar_consulta(query)
    
    def actualizar_administrador(self, id_admin, nombre, telefono, contrasena=None):
        if contrasena:
            query = "UPDATE administrador SET nombre = ?, telefono = ?, contrasena = ? WHERE id_administrador = ?"
            return self.db.ejecutar_actualizacion(query, (nombre, telefono, contrasena, id_admin))
        else:
            query = "UPDATE administrador SET nombre = ?, telefono = ? WHERE id_administrador = ?"
            return self.db.ejecutar_actualizacion(query, (nombre, telefono, id_admin))
    
    def eliminar_administrador(self, id_admin):
        query = "UPDATE administrador SET activo = 0 WHERE id_administrador = ?"
        return self.db.ejecutar_actualizacion(query, (id_admin,))
    
    def reactivar_administrador(self, id_admin):
        query = "UPDATE administrador SET activo = 1 WHERE id_administrador = ?"
        return self.db.ejecutar_actualizacion(query, (id_admin,))
    
    # --- Consultas para pacientes ---

    def obtener_pacientes(self, id_admin):
        query = "SELECT * FROM pacientes WHERE id_admin = ? AND activo = 1"
        return self.db.ejecutar_consulta(query, (id_admin,))
    
    def agregar_paciente(self, nombre, dieta, peso, id_admin):
        query = "INSERT INTO pacientes (nombre, dieta, peso, id_admin, activo) VALUES (?, ?, ?, ?, 1)"
        return self.db.ejecutar_actualizacion(query, (nombre, dieta, peso, id_admin))
    
    def actualizar_paciente(self, id_paciente, nombre, dieta, peso):
        query = "UPDATE pacientes SET nombre = ?, dieta = ?, peso = ? WHERE id_paciente = ?"
        return self.db.ejecutar_actualizacion(query, (nombre, dieta, peso, id_paciente))
    
    def eliminar_paciente(self, id_paciente):
        query = "UPDATE pacientes SET activo = 0 WHERE id_paciente = ?"
        return self.db.ejecutar_actualizacion(query, (id_paciente,))
    
    # --- Consultas para citas ---

    def obtener_citas(self, id_admin):
        # Nota: SQLite no tiene TIME_FORMAT, usamos strftime o tomamos la columna directa si ya es texto HH:MM
        query = """
        SELECT c.id_cita, p.nombre, p.peso, h.dia_semana, 
               h.hora as hora_cita,
               c.fecha, h.id_horario
        FROM citas c 
        JOIN pacientes p ON c.id_paciente = p.id_paciente
        JOIN horarios_disponibles h ON c.id_horario = h.id_horario
        WHERE p.id_admin = ? AND p.activo = 1
        """
        return self.db.ejecutar_consulta(query, (id_admin,))
    
    def agregar_cita(self, id_paciente, id_horario, fecha, hora_cita):
        query = "INSERT INTO citas (id_paciente, id_horario, fecha, hora_cita) VALUES (?, ?, ?, ?)"
        return self.db.ejecutar_actualizacion(query, (id_paciente, id_horario, fecha, hora_cita))
    
    def actualizar_cita(self, id_cita, id_paciente, id_horario, fecha, hora_cita):
        query = "UPDATE citas SET id_paciente = ?, id_horario = ?, fecha = ?, hora_cita = ? WHERE id_cita = ?"
        return self.db.ejecutar_actualizacion(query, (id_paciente, id_horario, fecha, hora_cita, id_cita))
    
    def eliminar_cita(self, id_cita):
        query = "DELETE FROM citas WHERE id_cita = ?"
        return self.db.ejecutar_actualizacion(query, (id_cita,))
    
    def obtener_horarios_disponibles(self):
        # Simulamos FIELD de MySQL con CASE WHEN para ordenar los días
        query = """
        SELECT id_horario, dia_semana, hora
        FROM horarios_disponibles 
        ORDER BY 
            CASE dia_semana
                WHEN 'Lunes' THEN 1
                WHEN 'Martes' THEN 2
                WHEN 'Miércoles' THEN 3
                WHEN 'Jueves' THEN 4
                WHEN 'Viernes' THEN 5
                WHEN 'Sábado' THEN 6
                WHEN 'Domingo' THEN 7
                ELSE 8
            END,
            hora
        """
        return self.db.ejecutar_consulta(query)
    
    def obtener_horarios_disponibles_por_fecha(self, fecha):
        dia_semana_map = {
            0: 'Lunes',
            1: 'Martes', 
            2: 'Miércoles',
            3: 'Jueves',
            4: 'Viernes',
            5: 'Sábado',
            6: 'Domingo'
        }
        
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
        dia_semana = dia_semana_map[fecha_obj.weekday()]
        
        query = """
        SELECT h.id_horario, h.dia_semana, h.hora
        FROM horarios_disponibles h
        WHERE h.dia_semana = ?
          AND h.id_horario NOT IN (
              SELECT id_horario FROM citas WHERE fecha = ?
          )
        ORDER BY h.hora
        """
        return self.db.ejecutar_consulta(query, (dia_semana, fecha))
    
    def generar_horarios_intervalo(self, hora_inicio, hora_fin, intervalo=10):
        from datetime import datetime, timedelta
        
        horarios = []
        inicio = datetime.strptime(hora_inicio, '%H:%M')
        fin = datetime.strptime(hora_fin, '%H:%M')
        
        while inicio < fin:
            horarios.append(inicio.strftime('%H:%M'))
            inicio += timedelta(minutes=intervalo)
        
        return horarios
    
    def eliminar_citas_por_paciente(self, id_paciente):
        query = "DELETE FROM citas WHERE id_paciente = ?"
        return self.db.ejecutar_actualizacion(query, (id_paciente,))
    
    def obtener_pacientes_con_citas(self, id_admin):
        query = """
        SELECT p.*, COUNT(c.id_cita) as total_citas
        FROM pacientes p 
        LEFT JOIN citas c ON p.id_paciente = c.id_paciente
        WHERE p.id_admin = ? AND p.activo = 1
        GROUP BY p.id_paciente
        """
        return self.db.ejecutar_consulta(query, (id_admin,))
    
    # --- Consultas para ingresos ---

    def obtener_ingresos_hoy(self, id_admin, fecha):
        # En SQLite guardamos la hora como texto HH:MM en el default, así que podemos leerla directo
        query = """
        SELECT i.*, i.hora as hora 
        FROM ingresos i 
        WHERE i.id_admin = ? AND i.fecha = ? 
        ORDER BY i.hora DESC
        """
        return self.db.ejecutar_consulta(query, (id_admin, fecha))
    
    def obtener_ingresos_por_fecha(self, id_admin, fecha):
        query = """
        SELECT i.*, i.hora as hora 
        FROM ingresos i 
        WHERE i.id_admin = ? AND i.fecha = ? 
        ORDER BY i.fecha DESC, i.hora DESC
        """
        return self.db.ejecutar_consulta(query, (id_admin, fecha))
    
    def agregar_ingreso(self, concepto, monto, fecha, id_admin):
        # La hora se inserta por defecto en la definición de tabla en conexion.py
        query = "INSERT INTO ingresos (concepto, monto, fecha, id_admin) VALUES (?, ?, ?, ?)"
        return self.db.ejecutar_actualizacion(query, (concepto, monto, fecha, id_admin))
    
    def actualizar_ingreso(self, id_ingreso, concepto, monto):
        query = "UPDATE ingresos SET concepto = ?, monto = ? WHERE id_ingreso = ?"
        return self.db.ejecutar_actualizacion(query, (concepto, monto, id_ingreso))
    
    def eliminar_ingreso(self, id_ingreso):
        query = "DELETE FROM ingresos WHERE id_ingreso = ?"
        return self.db.ejecutar_actualizacion(query, (id_ingreso,))
    
    def eliminar_ingresos_hoy(self, fecha, id_admin):
        query = "DELETE FROM ingresos WHERE fecha = ? AND id_admin = ?"
        return self.db.ejecutar_actualizacion(query, (fecha, id_admin))
    
    def obtener_total_ingresos_hoy(self, id_admin, fecha):
        query = "SELECT SUM(monto) as total FROM ingresos WHERE id_admin = ? AND fecha = ?"
        resultado = self.db.ejecutar_consulta(query, (id_admin, fecha))
        # Validar si resultado[0]['total'] es None
        return resultado[0]['total'] if resultado and resultado[0]['total'] else 0