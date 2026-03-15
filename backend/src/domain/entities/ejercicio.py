"""
Entidad: Ejercicio
==================
Representa un ejercicio de rehabilitación o terapia ocupacional
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from uuid import uuid4

from ..exceptions.domain_exceptions import InvalidEjercicioDataException


class TipoEjercicio(Enum):
    """Tipos de ejercicios disponibles en el sistema"""
    REHABILITACION = "rehabilitacion"
    TERAPIA_OCUPACIONAL = "terapia_ocupacional"
    EQUILIBRIO = "equilibrio"
    COORDINACION = "coordinacion"


class NivelDificultad(Enum):
    """Niveles de dificultad de los ejercicios"""
    PRINCIPIANTE = 1
    INTERMEDIO = 2
    AVANZADO = 3


@dataclass
class Ejercicio:
    """
    Entidad Ejercicio - Representa un ejercicio en el sistema
    
    Reglas de negocio:
    - Debe tener un nombre único
    - Debe tener instrucciones claras
    - Los parámetros deben ser válidos
    - Solo los ejercicios activos se pueden ejecutar
    """
    
    nombre: str
    descripcion: str
    tipo: TipoEjercicio
    nivel: NivelDificultad
    instrucciones: List[str]
    parametros: Dict
    id: str = field(default_factory=lambda: str(uuid4()))
    activo: bool = True
    duracion_estimada_minutos: Optional[int] = None
    
    def __post_init__(self):
        """Valida las reglas de negocio al crear el ejercicio"""
        self._validar()
    
    def _validar(self):
        """Valida las reglas de negocio del ejercicio"""
        if not self.nombre or not self.nombre.strip():
            raise InvalidEjercicioDataException("El nombre del ejercicio no puede estar vacío")
        
        if not self.descripcion or not self.descripcion.strip():
            raise InvalidEjercicioDataException("La descripción no puede estar vacía")
        
        if not self.instrucciones or len(self.instrucciones) == 0:
            raise InvalidEjercicioDataException("El ejercicio debe tener al menos una instrucción")
        
        if self.duracion_estimada_minutos is not None:
            if self.duracion_estimada_minutos <= 0:
                raise InvalidEjercicioDataException("La duración debe ser mayor a 0")
            if self.duracion_estimada_minutos > 120:
                raise InvalidEjercicioDataException("La duración no puede exceder 120 minutos")
    
    def activar(self) -> None:
        """Activa el ejercicio para que pueda ser usado"""
        self.activo = True
    
    def desactivar(self) -> None:
        """Desactiva el ejercicio temporalmente"""
        self.activo = False
    
    def actualizar_descripcion(self, nueva_descripcion: str) -> None:
        """Actualiza la descripción del ejercicio"""
        if not nueva_descripcion or not nueva_descripcion.strip():
            raise InvalidEjercicioDataException("La descripción no puede estar vacía")
        self.descripcion = nueva_descripcion
    
    def agregar_instruccion(self, instruccion: str) -> None:
        """Agrega una nueva instrucción al ejercicio"""
        if not instruccion or not instruccion.strip():
            raise InvalidEjercicioDataException("La instrucción no puede estar vacía")
        self.instrucciones.append(instruccion)
    
    def actualizar_parametro(self, clave: str, valor: any) -> None:
        """Actualiza un parámetro del ejercicio"""
        self.parametros[clave] = valor
    
    def es_ejecutable(self) -> bool:
        """Verifica si el ejercicio puede ser ejecutado"""
        return self.activo
    
    def es_para_principiantes(self) -> bool:
        """Verifica si el ejercicio es para principiantes"""
        return self.nivel == NivelDificultad.PRINCIPIANTE
    
    def __eq__(self, other) -> bool:
        """Dos ejercicios son iguales si tienen el mismo ID"""
        if not isinstance(other, Ejercicio):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash basado en el ID del ejercicio"""
        return hash(self.id)

