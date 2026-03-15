"""
Entidad: Sesión
===============
Representa una sesión de terapia completa
"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timedelta
from enum import Enum
from uuid import uuid4

from ..exceptions.domain_exceptions import InvalidSesionStateException


class EstadoSesion(Enum):
    """Estados posibles de una sesión"""
    PENDIENTE = "pendiente"
    CALENTAMIENTO = "calentamiento"
    EN_CURSO = "en_curso"
    PAUSA = "pausa"
    ENFRIAMIENTO = "enfriamiento"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"


@dataclass
class Sesion:
    """
    Entidad Sesión - Gestiona el ciclo de vida de una sesión de terapia
    
    Reglas de negocio:
    - Una sesión debe pasar por calentamiento antes de comenzar
    - No se puede pausar una sesión que no está en curso
    - Debe tener enfriamiento antes de completarse
    - El tiempo máximo de sesión no debe exceder límites de seguridad
    """
    
    paciente_id: str
    ejercicio_id: str
    id: str = field(default_factory=lambda: str(uuid4()))
    estado: EstadoSesion = EstadoSesion.PENDIENTE
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    duracion_minutos: int = 0
    calentamiento_completado: bool = False
    enfriamiento_completado: bool = False
    pausas_tomadas: int = 0
    alertas_descanso: int = 0
    nivel_fatiga: Optional[int] = None  # 1-5
    nivel_dolor: Optional[int] = None   # 0-10
    
    def iniciar(self) -> None:
        """Inicia la sesión comenzando con el calentamiento"""
        if self.estado != EstadoSesion.PENDIENTE:
            raise InvalidSesionStateException(
                f"No se puede iniciar una sesión en estado {self.estado.value}"
            )
        
        self.fecha_inicio = datetime.now()
        self.estado = EstadoSesion.CALENTAMIENTO
    
    def completar_calentamiento(self) -> None:
        """Marca el calentamiento como completado y pasa a ejercicios"""
        if self.estado != EstadoSesion.CALENTAMIENTO:
            raise InvalidSesionStateException(
                "Solo se puede completar calentamiento si la sesión está en ese estado"
            )
        
        self.calentamiento_completado = True
        self.estado = EstadoSesion.EN_CURSO
    
    def pausar(self) -> None:
        """Pausa la sesión actual"""
        if self.estado != EstadoSesion.EN_CURSO:
            raise InvalidSesionStateException(
                "Solo se puede pausar una sesión en curso"
            )
        
        self.estado = EstadoSesion.PAUSA
        self.pausas_tomadas += 1
    
    def reanudar(self) -> None:
        """Reanuda una sesión pausada"""
        if self.estado != EstadoSesion.PAUSA:
            raise InvalidSesionStateException(
                "Solo se puede reanudar una sesión pausada"
            )
        
        self.estado = EstadoSesion.EN_CURSO
    
    def iniciar_enfriamiento(self) -> None:
        """Inicia la fase de enfriamiento"""
        if self.estado != EstadoSesion.EN_CURSO:
            raise InvalidSesionStateException(
                "Solo se puede iniciar enfriamiento desde una sesión en curso"
            )
        
        if not self.calentamiento_completado:
            raise InvalidSesionStateException(
                "Debe completar el calentamiento antes de finalizar"
            )
        
        self.estado = EstadoSesion.ENFRIAMIENTO
    
    def completar_enfriamiento(self) -> None:
        """Completa el enfriamiento y finaliza la sesión"""
        if self.estado != EstadoSesion.ENFRIAMIENTO:
            raise InvalidSesionStateException(
                "Solo se puede completar enfriamiento si la sesión está en ese estado"
            )
        
        self.enfriamiento_completado = True
        self.finalizar()
    
    def finalizar(self) -> None:
        """Finaliza la sesión"""
        if self.estado == EstadoSesion.COMPLETADA or self.estado == EstadoSesion.CANCELADA:
            raise InvalidSesionStateException(
                "La sesión ya está finalizada"
            )
        
        self.fecha_fin = datetime.now()
        self.estado = EstadoSesion.COMPLETADA
        
        if self.fecha_inicio:
            duracion = self.fecha_fin - self.fecha_inicio
            self.duracion_minutos = int(duracion.total_seconds() / 60)
    
    def cancelar(self, motivo: Optional[str] = None) -> None:
        """Cancela la sesión"""
        if self.estado == EstadoSesion.COMPLETADA:
            raise InvalidSesionStateException(
                "No se puede cancelar una sesión completada"
            )
        
        self.fecha_fin = datetime.now()
        self.estado = EstadoSesion.CANCELADA
    
    def registrar_alerta_descanso(self) -> None:
        """Registra que se emitió una alerta de descanso"""
        self.alertas_descanso += 1
    
    def registrar_encuesta(self, nivel_fatiga: int, nivel_dolor: int) -> None:
        """Registra los resultados de la encuesta post-sesión"""
        if not (1 <= nivel_fatiga <= 5):
            raise ValueError("El nivel de fatiga debe estar entre 1 y 5")
        
        if not (0 <= nivel_dolor <= 10):
            raise ValueError("El nivel de dolor debe estar entre 0 y 10")
        
        self.nivel_fatiga = nivel_fatiga
        self.nivel_dolor = nivel_dolor
    
    def tiempo_transcurrido(self) -> int:
        """Retorna el tiempo transcurrido en minutos"""
        if not self.fecha_inicio:
            return 0
        
        fecha_referencia = self.fecha_fin if self.fecha_fin else datetime.now()
        duracion = fecha_referencia - self.fecha_inicio
        return int(duracion.total_seconds() / 60)
    
    def requiere_descanso(self, intervalo_minutos: int = 10) -> bool:
        """Verifica si se requiere un descanso según el tiempo transcurrido"""
        if self.estado != EstadoSesion.EN_CURSO:
            return False
        
        tiempo = self.tiempo_transcurrido()
        descansos_esperados = tiempo // intervalo_minutos
        return descansos_esperados > self.alertas_descanso
    
    def excede_limite_seguridad(self, limite_minutos: int = 30) -> bool:
        """Verifica si la sesión excede el límite de seguridad"""
        return self.tiempo_transcurrido() >= limite_minutos
    
    def puede_continuar(self) -> bool:
        """Verifica si la sesión puede continuar de forma segura"""
        if self.nivel_fatiga and self.nivel_fatiga >= 4:
            return False
        
        if self.nivel_dolor and self.nivel_dolor >= 7:
            return False
        
        return self.estado in [EstadoSesion.EN_CURSO, EstadoSesion.PAUSA]
    
    def __eq__(self, other) -> bool:
        """Dos sesiones son iguales si tienen el mismo ID"""
        if not isinstance(other, Sesion):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash basado en el ID de la sesión"""
        return hash(self.id)

