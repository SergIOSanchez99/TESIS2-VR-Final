"""
Value Object: ResultadoEjercicio
=================================
Representa el resultado de un ejercicio completado
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass(frozen=True)
class ResultadoEjercicio:
    """
    Value Object ResultadoEjercicio - Inmutable
    
    Representa el resultado de un ejercicio con todas sus métricas
    """
    
    paciente_id: str
    ejercicio_id: str
    sesion_id: str
    exito: bool
    fecha: datetime
    tiempo_ejecucion_segundos: int
    puntuacion: int
    
    # Métricas avanzadas
    precision: Optional[float] = None  # 0-100
    velocidad_promedio: Optional[float] = None
    rango_movimiento: Optional[float] = None
    tiempo_reaccion_promedio: Optional[float] = None
    tasa_aciertos: Optional[float] = None
    consistencia: Optional[float] = None
    combo_maximo: Optional[int] = None
    aciertos: Optional[int] = None
    fallos: Optional[int] = None
    
    def __post_init__(self):
        """Valida las métricas del resultado"""
        if self.tiempo_ejecucion_segundos < 0:
            raise ValueError("El tiempo de ejecución no puede ser negativo")
        
        if self.puntuacion < 0:
            raise ValueError("La puntuación no puede ser negativa")
        
        if self.precision is not None:
            if not (0 <= self.precision <= 100):
                raise ValueError("La precisión debe estar entre 0 y 100")
        
        if self.tasa_aciertos is not None:
            if not (0 <= self.tasa_aciertos <= 100):
                raise ValueError("La tasa de aciertos debe estar entre 0 y 100")
    
    def es_exitoso(self) -> bool:
        """Verifica si el ejercicio fue exitoso"""
        return self.exito
    
    def tiene_buena_precision(self, umbral: float = 80.0) -> bool:
        """Verifica si la precisión supera un umbral"""
        if self.precision is None:
            return False
        return self.precision >= umbral
    
    def es_rapido(self, limite_segundos: int = 60) -> bool:
        """Verifica si el ejercicio fue completado rápidamente"""
        return self.tiempo_ejecucion_segundos <= limite_segundos
    
    def calidad_del_resultado(self) -> str:
        """Retorna una evaluación cualitativa del resultado"""
        if not self.exito:
            return "FALLIDO"
        
        if self.precision is None:
            return "EXITOSO"
        
        if self.precision >= 95:
            return "EXCELENTE"
        elif self.precision >= 85:
            return "MUY_BUENO"
        elif self.precision >= 70:
            return "BUENO"
        else:
            return "REGULAR"

