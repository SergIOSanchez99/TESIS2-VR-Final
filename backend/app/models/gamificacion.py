"""
Modelo de Gamificación - Sistema de puntos, logros y recompensas
"""
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime, date
from enum import Enum


class TipoLogro(Enum):
    """Tipos de logros disponibles"""
    SESIONES = "sesiones"
    PRECISION = "precision"
    RACHA = "racha"
    ESPECIAL = "especial"


@dataclass
class Logro:
    """Clase de datos para representar un logro"""
    codigo: str
    nombre: str
    descripcion: str
    icono: str
    puntos_recompensa: int
    tipo: TipoLogro
    requisito_valor: int
    id: Optional[int] = None
    
    def to_dict(self) -> Dict:
        """Convierte el logro a diccionario"""
        data = asdict(self)
        data['tipo'] = self.tipo.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Logro':
        """Crea un logro desde un diccionario"""
        if isinstance(data.get('tipo'), str):
            data['tipo'] = TipoLogro(data['tipo'])
        return cls(**data)


@dataclass
class LogroPaciente:
    """Clase de datos para representar el progreso de un logro de un paciente"""
    paciente_id: int
    logro_id: int
    progreso_actual: int
    completado: bool
    fecha_obtencion: Optional[str] = None
    id: Optional[int] = None
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'LogroPaciente':
        """Crea desde un diccionario"""
        return cls(**data)


@dataclass
class GamificacionPaciente:
    """Clase de datos para representar la gamificación de un paciente"""
    paciente_id: int
    puntos_totales: int = 0
    nivel_actual: int = 1
    experiencia_actual: int = 0
    experiencia_siguiente_nivel: int = 100
    racha_dias: int = 0
    ultima_actividad: Optional[date] = None
    avatar_seleccionado: str = 'default'
    id: Optional[int] = None
    
    def agregar_experiencia(self, exp: int) -> bool:
        """
        Agrega experiencia y verifica si sube de nivel
        
        Returns:
            bool: True si subió de nivel
        """
        self.experiencia_actual += exp
        subio_nivel = False
        
        while self.experiencia_actual >= self.experiencia_siguiente_nivel:
            self.experiencia_actual -= self.experiencia_siguiente_nivel
            self.nivel_actual += 1
            self.experiencia_siguiente_nivel = int(self.experiencia_siguiente_nivel * 1.5)
            subio_nivel = True
        
        return subio_nivel
    
    def agregar_puntos(self, puntos: int):
        """Agrega puntos al total"""
        self.puntos_totales += puntos
    
    def actualizar_racha(self):
        """Actualiza la racha de días consecutivos"""
        hoy = date.today()
        
        if self.ultima_actividad is None:
            self.racha_dias = 1
        elif self.ultima_actividad == hoy:
            # Ya jugó hoy, no hacer nada
            pass
        elif (hoy - self.ultima_actividad).days == 1:
            # Día consecutivo
            self.racha_dias += 1
        else:
            # Se rompió la racha
            self.racha_dias = 1
        
        self.ultima_actividad = hoy
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario"""
        data = asdict(self)
        if isinstance(self.ultima_actividad, date):
            data['ultima_actividad'] = self.ultima_actividad.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GamificacionPaciente':
        """Crea desde un diccionario"""
        if 'ultima_actividad' in data and isinstance(data['ultima_actividad'], str):
            data['ultima_actividad'] = date.fromisoformat(data['ultima_actividad'])
        return cls(**data)


@dataclass
class ObjetivoDiario:
    """Clase de datos para representar un objetivo diario"""
    paciente_id: int
    fecha: date
    objetivo_sesiones: int = 1
    sesiones_completadas: int = 0
    objetivo_tiempo_minutos: int = 15
    tiempo_completado_minutos: int = 0
    completado: bool = False
    id: Optional[int] = None
    
    def registrar_sesion(self, duracion_minutos: int):
        """Registra una sesión completada"""
        self.sesiones_completadas += 1
        self.tiempo_completado_minutos += duracion_minutos
        self._verificar_completado()
    
    def _verificar_completado(self):
        """Verifica si el objetivo está completado"""
        self.completado = (
            self.sesiones_completadas >= self.objetivo_sesiones and
            self.tiempo_completado_minutos >= self.objetivo_tiempo_minutos
        )
    
    def progreso_sesiones(self) -> float:
        """Retorna el progreso de sesiones como porcentaje"""
        return min(100.0, (self.sesiones_completadas / self.objetivo_sesiones) * 100)
    
    def progreso_tiempo(self) -> float:
        """Retorna el progreso de tiempo como porcentaje"""
        return min(100.0, (self.tiempo_completado_minutos / self.objetivo_tiempo_minutos) * 100)
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario"""
        data = asdict(self)
        if isinstance(self.fecha, date):
            data['fecha'] = self.fecha.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ObjetivoDiario':
        """Crea desde un diccionario"""
        if 'fecha' in data and isinstance(data['fecha'], str):
            data['fecha'] = date.fromisoformat(data['fecha'])
        return cls(**data)


# Logros predefinidos
LOGROS_PREDEFINIDOS = [
    Logro(
        codigo="primera_sesion",
        nombre="Primer Paso",
        descripcion="Completa tu primera sesión de terapia",
        icono="star",
        puntos_recompensa=50,
        tipo=TipoLogro.SESIONES,
        requisito_valor=1
    ),
    Logro(
        codigo="cinco_sesiones",
        nombre="Constante",
        descripcion="Completa 5 sesiones de terapia",
        icono="fire",
        puntos_recompensa=100,
        tipo=TipoLogro.SESIONES,
        requisito_valor=5
    ),
    Logro(
        codigo="diez_sesiones",
        nombre="Dedicado",
        descripcion="Completa 10 sesiones de terapia",
        icono="medal",
        puntos_recompensa=200,
        tipo=TipoLogro.SESIONES,
        requisito_valor=10
    ),
    Logro(
        codigo="veinte_sesiones",
        nombre="Comprometido",
        descripcion="Completa 20 sesiones de terapia",
        icono="trophy",
        puntos_recompensa=500,
        tipo=TipoLogro.SESIONES,
        requisito_valor=20
    ),
    Logro(
        codigo="precision_80",
        nombre="Ojo de Águila",
        descripcion="Alcanza 80% de precisión en un ejercicio",
        icono="bullseye",
        puntos_recompensa=150,
        tipo=TipoLogro.PRECISION,
        requisito_valor=80
    ),
    Logro(
        codigo="precision_95",
        nombre="Maestro de la Precisión",
        descripcion="Alcanza 95% de precisión en un ejercicio",
        icono="crown",
        puntos_recompensa=300,
        tipo=TipoLogro.PRECISION,
        requisito_valor=95
    ),
    Logro(
        codigo="racha_3",
        nombre="Tres Días Seguidos",
        descripcion="Mantén una racha de 3 días consecutivos",
        icono="calendar-check",
        puntos_recompensa=100,
        tipo=TipoLogro.RACHA,
        requisito_valor=3
    ),
    Logro(
        codigo="racha_7",
        nombre="Una Semana Completa",
        descripcion="Mantén una racha de 7 días consecutivos",
        icono="calendar-week",
        puntos_recompensa=250,
        tipo=TipoLogro.RACHA,
        requisito_valor=7
    ),
    Logro(
        codigo="racha_30",
        nombre="Mes de Oro",
        descripcion="Mantén una racha de 30 días consecutivos",
        icono="gem",
        puntos_recompensa=1000,
        tipo=TipoLogro.RACHA,
        requisito_valor=30
    ),
    Logro(
        codigo="velocista",
        nombre="Velocista",
        descripcion="Completa un ejercicio en menos de 30 segundos",
        icono="bolt",
        puntos_recompensa=100,
        tipo=TipoLogro.ESPECIAL,
        requisito_valor=30
    )
]

