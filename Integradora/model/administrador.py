# Modulo encargado de controlar las operaciones dentro de administradores.

from base_datos.consultas import ConsultasDB

class Administrador:
    def __init__(self):
        self.consultas = ConsultasDB()
    
    def login(self, correo, contrasena):
        resultado = self.consultas.verificar_administrador(correo, contrasena)
        return len(resultado) > 0
    
    def registrar(self, nombre, telefono, correo, contrasena):
        # Asegurar que el teléfono sea string
        telefono_str = str(telefono)
        return self.consultas.registrar_administrador(nombre, telefono_str, correo, contrasena)
    
    def verificar_correo_existente(self, correo):
        resultado = self.consultas.verificar_correo_existente(correo)
        return len(resultado) > 0
    
    def obtener_id_administrador(self, correo):
        query = "SELECT id_administrador FROM administrador WHERE correo = %s AND activo = 1"
        resultado = self.consultas.db.ejecutar_consulta(query, (correo,))
        return resultado[0]['id_administrador'] if resultado else None
    
    def obtener_nombre_administrador(self, correo):
        query = "SELECT nombre FROM administrador WHERE correo = %s AND activo = 1"
        resultado = self.consultas.db.ejecutar_consulta(query, (correo,))
        return resultado[0]['nombre'] if resultado else None
    
    def obtener_todos(self):
        return self.consultas.obtener_administradores()
    
    def actualizar(self, id_admin, nombre, telefono, contrasena=None):
        # Asegurar que el teléfono sea string
        telefono_str = str(telefono)
        return self.consultas.actualizar_administrador(id_admin, nombre, telefono_str, contrasena)
    
    def eliminar(self, id_admin):
        return self.consultas.eliminar_administrador(id_admin)
    
    def reactivar(self, id_admin):
        return self.consultas.reactivar_administrador(id_admin)