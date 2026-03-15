"""
Interface: SesionRepository
============================
Define el contrato para el repositorio de sesiones
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from ..entities.sesion import Sesion, EstadoSesion


class ISesionRepository(ABC):
    """Interface del repositorio de sesiones"""
    
    @abstractmethod
    def guardar(self, sesion: Sesion) -> Sesion:
        """Guarda o actualiza una sesión"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, sesion_id: str) -> Optional[Sesion]:
        """Obtiene una sesión por su ID"""
        pass
    
    @abstractmethod
    def obtener_por_paciente(self, paciente_id: str) -> List[Sesion]:
        """Obtiene todas las sesiones de un paciente"""
        pass
    
    @abstractmethod
    def obtener_por_estado(self, estado: EstadoSesion) -> List[Sesion]:
        """Obtiene sesiones filtradas por estado"""
        pass
    
    @abstractmethod
    def obtener_activas(self) -> List[Sesion]:
        """Obtiene las sesiones actualmente en curso"""
        pass
    
    @abstractmethod
    def obtener_por_fecha_rango(
        self, 
        fecha_inicio: datetime, 
        fecha_fin: datetime
    ) -> List[Sesion]:
        """Obtiene sesiones en un rango de fechas"""
        pass
    
    @abstractmethod
    def obtener_sesion_activa_paciente(self, paciente_id: str) -> Optional[Sesion]:
        """Obtiene la sesión activa de un paciente si existe"""
        pass
    
    @abstractmethod
    def contar_por_paciente(self, paciente_id: str) -> int:
        """Cuenta las sesiones de un paciente"""
        pass

