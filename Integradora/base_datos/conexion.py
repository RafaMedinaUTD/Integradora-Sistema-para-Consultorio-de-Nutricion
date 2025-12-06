import mysql.connector
from mysql.connector import Error
from configuracion import Configuracion

class ConexionDB:
    def __init__(self):
        self.config = Configuracion.BASE_DATOS
    
    def conectar(self):
        try:
            conexion = mysql.connector.connect(
                host=self.config["host"],
                user=self.config["user"],
                password=self.config["password"],
                database=self.config["database"]
            )
            return conexion
        except Error as e:
            raise Exception(f"Error de conexión: {str(e)}")
    
    def ejecutar_consulta(self, query, params=None):
        conexion = self.conectar()
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(query, params or ())
            resultado = cursor.fetchall()
            conexion.commit()
            return resultado
        except Error as e:
            raise Exception(f"Error en consulta: {str(e)}")
        finally:
            cursor.close()
            conexion.close()
    
    def ejecutar_actualizacion(self, query, params=None):
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute(query, params or ())
            conexion.commit()
            return cursor.rowcount
        except Error as e:
            raise Exception(f"Error en actualización: {str(e)}")
        finally:
            cursor.close()
            conexion.close()