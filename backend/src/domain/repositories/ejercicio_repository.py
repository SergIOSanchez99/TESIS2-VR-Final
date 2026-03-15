"""
Interface: EjercicioRepository
===============================
Define el contrato para el repositorio de ejercicios
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.ejercicio import Ejercicio, TipoEjercicio, NivelDificultad


class IEjercicioRepository(ABC):
    """Interface del repositorio de ejercicios"""
    
    @abstractmethod
    def guardar(self, ejercicio: Ejercicio) -> Ejercicio:
        """Guarda o actualiza un ejercicio"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, ejercicio_id: str) -> Optional[Ejercicio]:
        """Obtiene un ejercicio por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Ejercicio]:
        """Obtiene todos los ejercicios"""
        pass
    
    @abstractmethod
    def obtener_activos(self) -> List[Ejercicio]:
        """Obtiene solo los ejercicios activos"""
        pass
    
    @abstractmethod
    def obtener_por_tipo(self, tipo: TipoEjercicio) -> List[Ejercicio]:
        """Obtiene ejercicios filtrados por tipo"""
        pass
    
    @abstractmethod
    def obtener_por_nivel(self, nivel: NivelDificultad) -> List[Ejercicio]:
        """Obtiene ejercicios filtrados por nivel de dificultad"""
        pass
    
    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Ejercicio]:
        """Busca ejercicios por nombre"""
        pass
    
    @abstractmethod
    def eliminar(self, ejercicio_id: str) -> bool:
        """Elimina un ejercicio (borrado lógico)"""
        pass

