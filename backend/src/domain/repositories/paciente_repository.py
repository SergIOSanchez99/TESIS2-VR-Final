"""
Interface: PacienteRepository
==============================
Define el contrato para el repositorio de pacientes
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.paciente import Paciente
from ..value_objects.email import Email


class IPacienteRepository(ABC):
    """
    Interface del repositorio de pacientes
    
    Define las operaciones que debe implementar cualquier repositorio concreto
    La implementación concreta estará en la capa de Infrastructure
    """
    
    @abstractmethod
    def guardar(self, paciente: Paciente) -> Paciente:
        """Guarda o actualiza un paciente"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, paciente_id: str) -> Optional[Paciente]:
        """Obtiene un paciente por su ID"""
        pass
    
    @abstractmethod
    def obtener_por_email(self, email: Email) -> Optional[Paciente]:
        """Obtiene un paciente por su email"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Paciente]:
        """Obtiene todos los pacientes"""
        pass
    
    @abstractmethod
    def obtener_activos(self) -> List[Paciente]:
        """Obtiene solo los pacientes activos"""
        pass
    
    @abstractmethod
    def existe_email(self, email: Email) -> bool:
        """Verifica si existe un paciente con ese email"""
        pass
    
    @abstractmethod
    def eliminar(self, paciente_id: str) -> bool:
        """Elimina un paciente (borrado lógico)"""
        pass
    
    @abstractmethod
    def contar_total(self) -> int:
        """Cuenta el total de pacientes"""
        pass

