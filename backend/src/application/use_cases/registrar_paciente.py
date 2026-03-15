"""
Use Case: Registrar Paciente
=============================
Caso de uso para registrar un nuevo paciente en el sistema
"""
from dataclasses import dataclass
from typing import Optional

from ...domain.entities.paciente import Paciente
from ...domain.value_objects.email import Email
from ...domain.value_objects.edad import Edad
from ...domain.repositories.paciente_repository import IPacienteRepository
from ...domain.exceptions.domain_exceptions import (
    EmailDuplicadoException,
    InvalidPacienteDataException
)


@dataclass
class RegistrarPacienteRequest:
    """DTO para la petición de registro de paciente"""
    nombre: str
    email: str
    password: str
    edad: int
    notas: Optional[str] = None


@dataclass
class RegistrarPacienteResponse:
    """DTO para la respuesta de registro de paciente"""
    paciente_id: str
    nombre: str
    email: str
    mensaje: str


class RegistrarPacienteUseCase:
    """
    Caso de uso: Registrar un nuevo paciente
    
    Reglas de negocio aplicadas:
    1. El email debe ser único en el sistema
    2. El email debe tener formato válido
    3. La edad debe estar en rango válido
    4. El nombre no puede estar vacío
    """
    
    def __init__(self, paciente_repository: IPacienteRepository):
        self.paciente_repository = paciente_repository
    
    def execute(self, request: RegistrarPacienteRequest) -> RegistrarPacienteResponse:
        """Ejecuta el caso de uso de registro de paciente"""
        
        # 1. Crear value objects (se auto-validan)
        email = Email(request.email)
        edad = Edad(request.edad)
        
        # 2. Verificar que el email no exista
        if self.paciente_repository.existe_email(email):
            raise EmailDuplicadoException(
                f"Ya existe un paciente registrado con el email {email.valor}"
            )
        
        # 3. Crear la entidad paciente (se auto-valida)
        paciente = Paciente(
            nombre=request.nombre,
            email=email,
            edad=edad,
            notas=request.notas
        )
        
        # 4. Guardar en el repositorio
        paciente_guardado = self.paciente_repository.guardar(paciente)
        
        # 5. Retornar respuesta
        return RegistrarPacienteResponse(
            paciente_id=paciente_guardado.id,
            nombre=paciente_guardado.nombre,
            email=paciente_guardado.email.valor,
            mensaje="Paciente registrado exitosamente"
        )

