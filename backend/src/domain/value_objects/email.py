"""
Value Object: Email
===================
Representa una dirección de correo electrónico válida
"""
import re
from dataclasses import dataclass

from ..exceptions.domain_exceptions import InvalidEmailException


@dataclass(frozen=True)
class Email:
    """
    Value Object Email - Inmutable y con validación
    
    Reglas:
    - Debe tener formato válido de email
    - No distingue mayúsculas/minúsculas
    - Es inmutable (frozen)
    """
    
    valor: str
    
    def __post_init__(self):
        """Valida el formato del email"""
        email_normalizado = self.valor.lower().strip()
        object.__setattr__(self, 'valor', email_normalizado)
        
        if not self._es_valido(email_normalizado):
            raise InvalidEmailException(f"Email inválido: {self.valor}")
    
    @staticmethod
    def _es_valido(email: str) -> bool:
        """Valida el formato del email usando expresión regular"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def __str__(self) -> str:
        return self.valor
    
    def __eq__(self, other) -> bool:
        """Igualdad por valor"""
        if not isinstance(other, Email):
            return False
        return self.valor == other.valor
    
    def __hash__(self) -> int:
        return hash(self.valor)

