"""
Modelo de Ejercicio - Patrón de Diseño Model
Responsable de la representación de datos y lógica de negocio de ejercicios
"""
import json
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class TipoEjercicio(Enum):
    """Tipos de ejercicios disponibles"""
    REHABILITACION = "rehabilitacion"
    TERAPIA_OCUPACIONAL = "terapia_ocupacional"


class NivelDificultad(Enum):
    """Niveles de dificultad"""
    PRINCIPIANTE = 1
    INTERMEDIO = 2
    AVANZADO = 3


@dataclass
class ResultadoEjercicio:
    """Clase de datos para representar un resultado de ejercicio"""
    paciente_id: str
    tipo_ejercicio: str
    nivel: int
    exito: bool
    fecha: str
    tiempo_ejecucion: Optional[float] = None
    puntuacion: Optional[int] = None
    observaciones: Optional[str] = None
    
    def __post_init__(self):
        if not self.fecha:
            self.fecha = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convierte el resultado a diccionario"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ResultadoEjercicio':
        """Crea un resultado desde un diccionario"""
        return cls(**data)


@dataclass
class Ejercicio:
    """Clase de datos para representar un ejercicio"""
    id: str
    nombre: str
    descripcion: str
    tipo: TipoEjercicio
    nivel: NivelDificultad
    instrucciones: List[str]
    parametros: Dict
    activo: bool = True
    
    def to_dict(self) -> Dict:
        """Convierte el ejercicio a diccionario"""
        data = asdict(self)
        data['tipo'] = self.tipo.value
        data['nivel'] = self.nivel.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Ejercicio':
        """Crea un ejercicio desde un diccionario"""
        data['tipo'] = TipoEjercicio(data['tipo'])
        data['nivel'] = NivelDificultad(data['nivel'])
        return cls(**data)


class EjercicioRepository:
    """Repositorio para manejo de datos de ejercicios - Patrón Repository"""
    
    def __init__(self, historial_path: str = "data/pacientes/historial"):
        self.historial_path = historial_path
    
    def registrar_resultado(self, paciente_id: str, ejercicio: str, exito: bool, 
                          tiempo_ejecucion: Optional[float] = None,
                          puntuacion: Optional[int] = None,
                          observaciones: Optional[str] = None) -> ResultadoEjercicio:
        """Registra un resultado de ejercicio"""
        resultado = ResultadoEjercicio(
            paciente_id=paciente_id,
            tipo_ejercicio=ejercicio,
            nivel=1,  # Por defecto, se puede mejorar
            exito=exito,
            tiempo_ejecucion=tiempo_ejecucion,
            puntuacion=puntuacion,
            observaciones=observaciones
        )
        
        # Guardar en el historial del paciente
        historial_file = f"{paciente_id}.json"
        historial_path = f"{self.historial_path}/{historial_file}"
        
        try:
            with open(historial_path, "r", encoding="utf-8") as f:
                historial = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            historial = []
        
        historial.append(resultado.to_dict())
        
        with open(historial_path, "w", encoding="utf-8") as f:
            json.dump(historial, f, ensure_ascii=False, indent=2)
        
        return resultado
    
    def obtener_historial(self, paciente_id: str) -> List[ResultadoEjercicio]:
        """Obtiene el historial de ejercicios de un paciente"""
        historial_file = f"{paciente_id}.json"
        historial_path = f"{self.historial_path}/{historial_file}"
        
        try:
            with open(historial_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [ResultadoEjercicio.from_dict(r) for r in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def obtener_estadisticas(self, paciente_id: str) -> Dict:
        """Obtiene estadísticas del paciente"""
        historial = self.obtener_historial(paciente_id)
        
        if not historial:
            return {
                'total_ejercicios': 0,
                'ejercicios_exitosos': 0,
                'porcentaje_exito': 0,
                'promedio_tiempo': 0,
                'ultima_actividad': None
            }
        
        total = len(historial)
        exitosos = sum(1 for r in historial if r.exito)
        porcentaje = (exitosos / total) * 100 if total > 0 else 0
        
        tiempos = [r.tiempo_ejecucion for r in historial if r.tiempo_ejecucion]
        promedio_tiempo = sum(tiempos) / len(tiempos) if tiempos else 0
        
        ultima_actividad = max(historial, key=lambda x: x.fecha).fecha if historial else None
        
        return {
            'total_ejercicios': total,
            'ejercicios_exitosos': exitosos,
            'porcentaje_exito': round(porcentaje, 2),
            'promedio_tiempo': round(promedio_tiempo, 2),
            'ultima_actividad': ultima_actividad
        }
