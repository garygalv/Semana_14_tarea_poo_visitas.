# modelos/visitante.py

class Visitante:
    """Clase que representa los datos de un visitante (Capa Modelo)"""
    
    def __init__(self, cedula: str, nombre: str, motivo: str):
        self.cedula = cedula
        self.nombre = nombre
        self.motivo = motivo
    
    def __str__(self):
        return f"{self.cedula} | {self.nombre} | {self.motivo}"