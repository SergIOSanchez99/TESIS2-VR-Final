"""
Entidad: Paciente
=================
Representa a un paciente del sistema con sus reglas de negocio fundamentales
"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from uuid import uuid4

from ..value_objects.email import Email
from ..value_objects.edad import Edad
from ..exceptions.domain_exceptions import InvalidPacienteDataException


@dataclass
class Paciente:
    """
    Entidad Paciente - Contiene la lógica de negocio fundamental
    
    Reglas de negocio:
    - Un paciente debe tener un email válido
    - La edad debe estar entre 0 y 120 años
    - El nombre no puede estar vacío
    - Cada paciente tiene un ID único (UUID)
    """
    
    nombre: str
    email: Email
    edad: Edad
    id: str = field(default_factory=lambda: str(uuid4()))
    fecha_registro: datetime = field(default_factory=datetime.now)
    activo: bool = True
    notas: Optional[str] = None
    
    def __post_init__(self):
        """Valida las reglas de negocio al crear/modificar la entidad"""
        self._validar()
    
    def _validar(self):
        """Valida las reglas de negocio del paciente"""
        if not self.nombre or not self.nombre.strip():
            raise InvalidPacienteDataException("El nombre del paciente no puede estar vacío")
        
        if len(self.nombre) < 2:
            raise InvalidPacienteDataException("El nombre debe tener al menos 2 caracteres")
        
        if len(self.nombre) > 100:
            raise InvalidPacienteDataException("El nombre no puede tener más de 100 caracteres")
    
    def activar(self) -> None:
        """Activa el paciente en el sistema"""
        self.activo = True
    
    def desactivar(self) -> None:
        """Desactiva el paciente en el sistema"""
        self.activo = False
    
    def actualizar_nombre(self, nuevo_nombre: str) -> None:
        """Actualiza el nombre del paciente validando las reglas de negocio"""
        nombre_anterior = self.nombre
        self.nombre = nuevo_nombre
        try:
            self._validar()
        except InvalidPacienteDataException:
            self.nombre = nombre_anterior  # Rollback
            raise
    
    def actualizar_notas(self, notas: str) -> None:
        """Actualiza las notas del paciente"""
        self.notas = notas
    
    def es_activo(self) -> bool:
        """Verifica si el paciente está activo"""
        return self.activo
    
    def __eq__(self, other) -> bool:
        """Dos pacientes son iguales si tienen el mismo ID"""
        if not isinstance(other, Paciente):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash basado en el ID del paciente"""
        return hash(self.id)

