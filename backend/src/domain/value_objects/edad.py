"""
Value Object: Edad
==================
Representa la edad de un paciente con validación
"""
from dataclasses import dataclass

from ..exceptions.domain_exceptions import InvalidEdadException


@dataclass(frozen=True)
class Edad:
    """
    Value Object Edad - Inmutable y con validación
    
    Reglas:
    - Debe ser un número entre 0 y 120
    - Es inmutable (frozen)
    """
    
    valor: int
    
    def __post_init__(self):
        """Valida que la edad esté en un rango válido"""
        if not isinstance(self.valor, int):
            raise InvalidEdadException("La edad debe ser un número entero")
        
        if self.valor < 0:
            raise InvalidEdadException("La edad no puede ser negativa")
        
        if self.valor > 120:
            raise InvalidEdadException("La edad no puede ser mayor a 120 años")
    
    def es_adulto(self) -> bool:
        """Verifica si la persona es adulta (18+)"""
        return self.valor >= 18
    
    def es_menor(self) -> bool:
        """Verifica si la persona es menor de edad"""
        return self.valor < 18
    
    def es_adulto_mayor(self) -> bool:
        """Verifica si la persona es adulto mayor (65+)"""
        return self.valor >= 65
    
    def __str__(self) -> str:
        return str(self.valor)
    
    def __eq__(self, other) -> bool:
        """Igualdad por valor"""
        if not isinstance(other, Edad):
            return False
        return self.valor == other.valor
    
    def __hash__(self) -> int:
        return hash(self.valor)
    
    def __lt__(self, other) -> bool:
        """Permite comparación de edades"""
        if not isinstance(other, Edad):
            return NotImplemented
        return self.valor < other.valor

