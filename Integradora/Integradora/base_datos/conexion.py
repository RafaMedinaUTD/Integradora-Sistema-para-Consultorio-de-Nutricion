# Integradora/base_datos/conexion.py

import sqlite3
import os
from configuracion import Configuracion

class ConexionDB:
    def __init__(self):
        self.config = Configuracion.BASE_DATOS
        self.db_name = self.config["database"]
        self.inicializar_base_datos()
    
    def conectar(self):
        """Metodo que permite conectar a la base de datos SQLite."""
        try:
            # Conecta o crea el archivo .db
            conexion = sqlite3.connect(self.db_name)
            # Esto permite acceder a las columnas por nombre (como diccionario)
            conexion.row_factory = sqlite3.Row 
            return conexion
        except sqlite3.Error as e:
            raise Exception(f"Error de conexión: {str(e)}")

    def inicializar_base_datos(self):
        """Crea las tablas necesarias si no existen."""
        sql_creation_script = """
        CREATE TABLE IF NOT EXISTS administrador (
            id_administrador INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            correo TEXT UNIQUE,
            contrasena TEXT,
            activo INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS pacientes (
            id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            dieta TEXT,
            peso REAL,
            id_admin INTEGER,
            activo INTEGER DEFAULT 1,
            FOREIGN KEY(id_admin) REFERENCES administrador(id_administrador)
        );

        CREATE TABLE IF NOT EXISTS horarios_disponibles (
            id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
            dia_semana TEXT,
            hora TEXT
        );

        CREATE TABLE IF NOT EXISTS citas (
            id_cita INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER,
            id_horario INTEGER,
            fecha TEXT,
            hora_cita TEXT,
            FOREIGN KEY(id_paciente) REFERENCES pacientes(id_paciente),
            FOREIGN KEY(id_horario) REFERENCES horarios_disponibles(id_horario)
        );

        CREATE TABLE IF NOT EXISTS ingresos (
            id_ingreso INTEGER PRIMARY KEY AUTOINCREMENT,
            concepto TEXT,
            monto REAL,
            fecha TEXT,
            hora TEXT DEFAULT (strftime('%H:%M', 'now', 'localtime')),
            id_admin INTEGER,
            FOREIGN KEY(id_admin) REFERENCES administrador(id_administrador)
        );
        """
        
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.executescript(sql_creation_script)
            
            # Poblar horarios si está vacío
            cursor.execute("SELECT count(*) FROM horarios_disponibles")
            if cursor.fetchone()[0] == 0:
                dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
                
                horas = []
                
                # --- Turno Matutino: 10:00 AM a 2:00 PM (14:00) ---
                for h in range(10, 14): # Genera 10, 11, 12, 13
                    for m in range(0, 60, 10): # Genera 00, 10, 20...
                        horas.append(f"{h:02d}:{m:02d}")
                horas.append("14:00") # Agregamos el límite de las 2 PM

                # --- Turno Vespertino: 4:00 PM (16:00) a 8:00 PM (20:00) ---
                for h in range(16, 20): # Genera 16, 17, 18, 19
                    for m in range(0, 60, 10):
                        horas.append(f"{h:02d}:{m:02d}")
                horas.append("20:00") # Agregamos el límite de las 8 PM

                # Insertar en la base de datos
                for dia in dias:
                    for hora in horas:
                        cursor.execute("INSERT INTO horarios_disponibles (dia_semana, hora) VALUES (?, ?)", (dia, hora))
            
            # Crear un admin por defecto si no existe ninguno
            cursor.execute("SELECT count(*) FROM administrador")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO administrador (nombre, correo, contrasena, activo) VALUES (?, ?, ?, 1)", 
                               ("Admin Inicial", "admin@email.com", "123456"))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error inicializando DB: {e}")

    
    def ejecutar_consulta(self, query, params=None):
        """Ejecuta una consulta SELECT y devuelve lista de diccionarios."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute(query, params or ())
            resultado = cursor.fetchall()
            return [dict(row) for row in resultado]
        except sqlite3.Error as e:
            raise Exception(f"Error en consulta: {str(e)}")
        finally:
            conexion.close()
    
    def ejecutar_actualizacion(self, query, params=None):
        """Ejecuta INSERT, UPDATE, DELETE."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute(query, params or ())
            conexion.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            raise Exception(f"Error en actualización: {str(e)}")
        finally:
            conexion.close()