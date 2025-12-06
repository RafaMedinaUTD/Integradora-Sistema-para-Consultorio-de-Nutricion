import re
from datetime import datetime

class Validaciones:
    @staticmethod
    def validar_correo(correo):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, correo) is not None
    
    @staticmethod
    def validar_fecha(fecha):
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_horario(horario):
        try:
            datetime.strptime(horario, '%H:%M')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_texto(texto):
        return len(texto.strip()) > 0
    
    @staticmethod
    def validar_telefono(telefono):
        return telefono.isdigit() and len(telefono) >= 10
    
    @staticmethod
    def validar_peso(peso):
        try:
            peso_float = float(peso)
            return peso_float > 0 and peso_float < 500  # Rango de peso humano para que no exagere
        except ValueError:
            return False