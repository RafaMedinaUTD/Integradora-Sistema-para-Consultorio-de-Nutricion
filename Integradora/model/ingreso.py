# Modulo encargado de controlar las operaciones dentro de ingresos.

from base_datos.consultas import ConsultasDB
from datetime import datetime

class Ingreso:
    def __init__(self):
        self.consultas = ConsultasDB()
    
    def obtener_todos_hoy(self, id_admin):
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        return self.consultas.obtener_ingresos_hoy(id_admin, fecha_hoy)
    
    def obtener_por_fecha(self, id_admin, fecha):
        return self.consultas.obtener_ingresos_por_fecha(id_admin, fecha)
    
    def crear(self, concepto, monto, id_admin):
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        return self.consultas.agregar_ingreso(concepto, monto, fecha_hoy, id_admin)
    
    def actualizar(self, id_ingreso, concepto, monto):
        return self.consultas.actualizar_ingreso(id_ingreso, concepto, monto)
    
    def eliminar(self, id_ingreso):
        return self.consultas.eliminar_ingreso(id_ingreso)
    
    def eliminar_todos_hoy(self, id_admin):
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        return self.consultas.eliminar_ingresos_hoy(fecha_hoy, id_admin)
    
    def obtener_total_hoy(self, id_admin):
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        return self.consultas.obtener_total_ingresos_hoy(id_admin, fecha_hoy)