from modelos.visitante import Visitante

class VisitaServicio:
    """Capa de Servicios - Lógica de negocio (CRUD)"""
    
    def __init__(self):
        self._visitantes: list[Visitante] = []   # Encapsulamiento (atributo privado)

    def registrar(self, visitante: Visitante) -> None:
        """Registra un visitante (valida cédula única)"""
        if any(v.cedula == visitante.cedula for v in self._visitantes):
            raise ValueError("La cédula ya está registrada.")
        self._visitantes.append(visitante)

    def obtener_todos(self) -> list[Visitante]:
        """Retorna copia de la lista (encapsulamiento)"""
        return self._visitantes[:]

    def eliminar(self, cedula: str) -> None:
        """Elimina visitante por cédula"""
        self._visitantes = [v for v in self._visitantes if v.cedula != cedula]