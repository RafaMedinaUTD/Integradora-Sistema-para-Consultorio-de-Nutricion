from base_datos.consultas import ConsultasDB

class Administrador:
    def __init__(self):
        self.consultas = ConsultasDB()
    
    def login(self, correo, contrasena):
        resultado = self.consultas.verificar_administrador(correo, contrasena)
        return len(resultado) > 0
    
    def registrar(self, nombre, telefono, correo, contrasena):
        return self.consultas.registrar_administrador(nombre, telefono, correo, contrasena)
    
    def verificar_correo_existente(self, correo):
        resultado = self.consultas.verificar_correo_existente(correo)
        return len(resultado) > 0
    
    def obtener_id_administrador(self, correo):
        query = "SELECT id_administrador FROM administrador WHERE correo = %s"
        resultado = self.consultas.db.ejecutar_consulta(query, (correo,))
        return resultado[0]['id_administrador'] if resultado else None
    
    def obtener_nombre_administrador(self, correo):
        query = "SELECT nombre FROM administrador WHERE correo = %s"
        resultado = self.consultas.db.ejecutar_consulta(query, (correo,))
        return resultado[0]['nombre'] if resultado else None