"""
Use Case: Iniciar Sesión de Terapia
====================================
Caso de uso para iniciar una nueva sesión de terapia
"""
from dataclasses import dataclass
from typing import List

from ...domain.entities.sesion import Sesion, EstadoSesion
from ...domain.repositories.sesion_repository import ISesionRepository
from ...domain.repositories.paciente_repository import IPacienteRepository
from ...domain.repositories.ejercicio_repository import IEjercicioRepository
from ...domain.exceptions.domain_exceptions import (
    PacienteNotFoundException,
    PacienteInactivoException,
    EjercicioNotFoundException,
    EjercicioInactivoException,
    InvalidSesionStateException
)


@dataclass
class IniciarSesionTerapiaRequest:
    """DTO para la petición de inicio de sesión"""
    paciente_id: str
    ejercicio_id: str


@dataclass
class IniciarSesionTerapiaResponse:
    """DTO para la respuesta de inicio de sesión"""
    sesion_id: str
    estado: str
    advertencias_seguridad: List[str]
    ejercicios_calentamiento: List[str]
    mensaje: str


class IniciarSesionTerapiaUseCase:
    """
    Caso de uso: Iniciar una nueva sesión de terapia
    
    Reglas de negocio aplicadas:
    1. El paciente debe existir y estar activo
    2. El ejercicio debe existir y estar activo
    3. No puede haber otra sesión activa del paciente
    4. Se debe mostrar advertencias de seguridad
    5. Se debe comenzar con calentamiento
    """
    
    def __init__(
        self,
        sesion_repository: ISesionRepository,
        paciente_repository: IPacienteRepository,
        ejercicio_repository: IEjercicioRepository
    ):
        self.sesion_repository = sesion_repository
        self.paciente_repository = paciente_repository
        self.ejercicio_repository = ejercicio_repository
    
    def execute(self, request: IniciarSesionTerapiaRequest) -> IniciarSesionTerapiaResponse:
        """Ejecuta el caso de uso de iniciar sesión"""
        
        # 1. Verificar que el paciente existe y está activo
        paciente = self.paciente_repository.obtener_por_id(request.paciente_id)
        if not paciente:
            raise PacienteNotFoundException(
                f"No se encontró el paciente con ID {request.paciente_id}"
            )
        
        if not paciente.es_activo():
            raise PacienteInactivoException(
                f"El paciente {paciente.nombre} está inactivo"
            )
        
        # 2. Verificar que el ejercicio existe y está activo
        ejercicio = self.ejercicio_repository.obtener_por_id(request.ejercicio_id)
        if not ejercicio:
            raise EjercicioNotFoundException(
                f"No se encontró el ejercicio con ID {request.ejercicio_id}"
            )
        
        if not ejercicio.es_ejecutable():
            raise EjercicioInactivoException(
                f"El ejercicio '{ejercicio.nombre}' no está disponible"
            )
        
        # 3. Verificar que no haya otra sesión activa
        sesion_activa = self.sesion_repository.obtener_sesion_activa_paciente(
            request.paciente_id
        )
        if sesion_activa:
            raise InvalidSesionStateException(
                "Ya existe una sesión activa. Debe finalizarla antes de iniciar otra."
            )
        
        # 4. Crear nueva sesión
        sesion = Sesion(
            paciente_id=request.paciente_id,
            ejercicio_id=request.ejercicio_id
        )
        
        # 5. Iniciar la sesión (comienza con calentamiento)
        sesion.iniciar()
        
        # 6. Guardar la sesión
        sesion_guardada = self.sesion_repository.guardar(sesion)
        
        # 7. Preparar advertencias de seguridad
        advertencias = [
            "Asegúrate de tener suficiente espacio alrededor",
            "Si sientes mareo, pausa inmediatamente la sesión",
            "Realiza los ejercicios de calentamiento antes de comenzar",
            "Si sientes dolor, detén el ejercicio"
        ]
        
        # 8. Ejercicios de calentamiento
        ejercicios_calentamiento = [
            "Rotación de Hombros (30s)",
            "Estiramiento de Brazos (30s)",
            "Rotación de Cuello (30s)",
            "Flexión de Muñecas (20s)"
        ]
        
        # 9. Retornar respuesta
        return IniciarSesionTerapiaResponse(
            sesion_id=sesion_guardada.id,
            estado=sesion_guardada.estado.value,
            advertencias_seguridad=advertencias,
            ejercicios_calentamiento=ejercicios_calentamiento,
            mensaje="Sesión iniciada correctamente. Por favor, realiza el calentamiento."
        )

