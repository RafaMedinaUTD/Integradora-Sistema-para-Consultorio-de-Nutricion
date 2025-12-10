# Modulo encargado de realizar las validaciones dentro del sistema.

import re
from datetime import datetime

class Validaciones:

    @staticmethod
    def validar_correo(correo): # Verifica que el correo use los caracteres correctos y la estructura comun: example@example.com
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, correo) is not None
    
    @staticmethod
    def validar_fecha(fecha): # Verifica que la fecha tenga el orden correcto y formato: 2025-03-12
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_horario(horario): # Verifica que el horario tenga un formato correcto: 12:30
        try:
            datetime.strptime(horario, '%H:%M')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_texto(texto): # Verifica que el texto sea mayor a 0 digitos.
        return len(texto.strip()) > 0
    
    @staticmethod
    def validar_telefono(telefono): # Verifica que el numero telefonico use solamente numeros y sea mayor o igual a 10 digitos.
        return telefono.isdigit() and len(telefono) >= 10
    
    @staticmethod
    def validar_peso(peso): # Verifica que el peso no exceda los 500 kilos (Rango de peso humano)
        try:
            peso_float = float(peso)
            return peso_float > 0 and peso_float < 500 
        except ValueError:
            return False