"""
Modelo de Sesión - Gestión de sesiones de terapia con seguridad y tracking
"""
from dataclasses import dataclass, asdict
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from enum import Enum


class EstadoSesion(Enum):
    """Estados posibles de una sesión"""
    PENDIENTE = "pendiente"
    CALENTAMIENTO = "calentamiento"
    EN_CURSO = "en_curso"
    PAUSA = "pausa"
    ENFRIAMIENTO = "enfriamiento"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"


class TipoTerapia(Enum):
    """Tipos de terapia disponibles"""
    REHABILITACION = "rehabilitacion"
    TERAPIA_OCUPACIONAL = "terapia_ocupacional"
    EQUILIBRIO = "equilibrio"
    COORDINACION = "coordinacion"
    MIXTA = "mixta"


@dataclass
class Sesion:
    """Clase de datos para representar una sesión de terapia"""
    paciente_id: int
    tipo_terapia: TipoTerapia
    duracion_minutos: int = 0
    fecha_sesion: Optional[datetime] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado: EstadoSesion = EstadoSesion.PENDIENTE
    calentamiento_completado: bool = False
    enfriamiento_completado: bool = False
    nivel_fatiga: Optional[int] = None  # 1-5
    nivel_dolor: Optional[int] = None  # 0-10
    alertas_descanso: int = 0
    pausas_tomadas: int = 0
    observaciones: Optional[str] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        if not self.fecha_sesion:
            self.fecha_sesion = datetime.now()
    
    def iniciar(self):
        """Inicia la sesión"""
        self.fecha_inicio = datetime.now()
        self.estado = EstadoSesion.CALENTAMIENTO
    
    def completar_calentamiento(self):
        """Marca el calentamiento como completado"""
        self.calentamiento_completado = True
        self.estado = EstadoSesion.EN_CURSO
    
    def pausar(self):
        """Pausa la sesión"""
        if self.estado == EstadoSesion.EN_CURSO:
            self.estado = EstadoSesion.PAUSA
            self.pausas_tomadas += 1
    
    def reanudar(self):
        """Reanuda la sesión"""
        if self.estado == EstadoSesion.PAUSA:
            self.estado = EstadoSesion.EN_CURSO
    
    def iniciar_enfriamiento(self):
        """Inicia el enfriamiento"""
        self.estado = EstadoSesion.ENFRIAMIENTO
    
    def completar_enfriamiento(self):
        """Marca el enfriamiento como completado"""
        self.enfriamiento_completado = True
        self.finalizar()
    
    def finalizar(self):
        """Finaliza la sesión"""
        self.fecha_fin = datetime.now()
        self.estado = EstadoSesion.COMPLETADA
        if self.fecha_inicio:
            self.duracion_minutos = int((self.fecha_fin - self.fecha_inicio).total_seconds() / 60)
    
    def cancelar(self):
        """Cancela la sesión"""
        self.estado = EstadoSesion.CANCELADA
        self.fecha_fin = datetime.now()
    
    def registrar_alerta_descanso(self):
        """Registra una alerta de descanso"""
        self.alertas_descanso += 1
    
    def registrar_encuesta(self, nivel_fatiga: int, nivel_dolor: int, observaciones: str = None):
        """Registra los resultados de la encuesta post-sesión"""
        self.nivel_fatiga = nivel_fatiga
        self.nivel_dolor = nivel_dolor
        if observaciones:
            self.observaciones = observaciones
    
    def tiempo_transcurrido(self) -> int:
        """Retorna el tiempo transcurrido en minutos"""
        if not self.fecha_inicio:
            return 0
        
        fecha_referencia = self.fecha_fin if self.fecha_fin else datetime.now()
        return int((fecha_referencia - self.fecha_inicio).total_seconds() / 60)
    
    def requiere_descanso(self, intervalo_minutos: int = 10) -> bool:
        """Verifica si se requiere un descanso"""
        if not self.fecha_inicio or self.estado != EstadoSesion.EN_CURSO:
            return False
        
        tiempo = self.tiempo_transcurrido()
        descansos_esperados = tiempo // intervalo_minutos
        return descansos_esperados > self.alertas_descanso
    
    def excede_limite_tiempo(self, limite_minutos: int = 30) -> bool:
        """Verifica si la sesión excede el límite de tiempo"""
        return self.tiempo_transcurrido() >= limite_minutos
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario"""
        data = asdict(self)
        data['tipo_terapia'] = self.tipo_terapia.value
        data['estado'] = self.estado.value
        
        # Convertir fechas a ISO format
        for campo in ['fecha_sesion', 'fecha_inicio', 'fecha_fin']:
            if isinstance(getattr(self, campo), datetime):
                data[campo] = getattr(self, campo).isoformat()
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Sesion':
        """Crea desde un diccionario"""
        # Convertir strings a enums
        if isinstance(data.get('tipo_terapia'), str):
            data['tipo_terapia'] = TipoTerapia(data['tipo_terapia'])
        if isinstance(data.get('estado'), str):
            data['estado'] = EstadoSesion(data['estado'])
        
        # Convertir fechas
        for campo in ['fecha_sesion', 'fecha_inicio', 'fecha_fin']:
            if campo in data and isinstance(data[campo], str):
                data[campo] = datetime.fromisoformat(data[campo])
        
        return cls(**data)


@dataclass
class EjercicioCalentamiento:
    """Ejercicio de calentamiento"""
    nombre: str
    descripcion: str
    duracion_segundos: int
    video_url: Optional[str] = None
    imagen_url: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class EjercicioEnfriamiento:
    """Ejercicio de enfriamiento"""
    nombre: str
    descripcion: str
    duracion_segundos: int
    video_url: Optional[str] = None
    imagen_url: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


# Ejercicios de calentamiento predefinidos
EJERCICIOS_CALENTAMIENTO = [
    EjercicioCalentamiento(
        nombre="Rotación de Hombros",
        descripcion="Realiza movimientos circulares con los hombros hacia adelante y hacia atrás",
        duracion_segundos=30
    ),
    EjercicioCalentamiento(
        nombre="Estiramiento de Brazos",
        descripcion="Extiende los brazos hacia adelante y hacia los lados suavemente",
        duracion_segundos=30
    ),
    EjercicioCalentamiento(
        nombre="Rotación de Cuello",
        descripcion="Gira la cabeza lentamente de lado a lado",
        duracion_segundos=30
    ),
    EjercicioCalentamiento(
        nombre="Flexión de Muñecas",
        descripcion="Realiza movimientos circulares con las muñecas",
        duracion_segundos=20
    )
]

# Ejercicios de enfriamiento predefinidos
EJERCICIOS_ENFRIAMIENTO = [
    EjercicioEnfriamiento(
        nombre="Respiración Profunda",
        descripcion="Inhala profundamente por la nariz y exhala por la boca",
        duracion_segundos=30
    ),
    EjercicioEnfriamiento(
        nombre="Estiramiento de Brazos",
        descripcion="Estira suavemente los brazos por encima de la cabeza",
        duracion_segundos=30
    ),
    EjercicioEnfriamiento(
        nombre="Relajación de Hombros",
        descripcion="Baja los hombros y relaja los músculos",
        duracion_segundos=20
    ),
    EjercicioEnfriamiento(
        nombre="Estiramiento Lateral",
        descripcion="Inclínate suavemente hacia cada lado",
        duracion_segundos=30
    )
]


@dataclass
class AlertaSeguridad:
    """Alerta de seguridad durante la sesión"""
    tipo: str  # 'descanso', 'limite_tiempo', 'movimiento_brusco', 'inactividad'
    mensaje: str
    timestamp: datetime
    severidad: str  # 'info', 'warning', 'danger'
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def crear_alerta_descanso(cls) -> 'AlertaSeguridad':
        """Crea una alerta de descanso"""
        return cls(
            tipo='descanso',
            mensaje='Es recomendable tomar un descanso de 2 minutos',
            timestamp=datetime.now(),
            severidad='warning'
        )
    
    @classmethod
    def crear_alerta_limite_tiempo(cls) -> 'AlertaSeguridad':
        """Crea una alerta de límite de tiempo"""
        return cls(
            tipo='limite_tiempo',
            mensaje='Has alcanzado el límite de tiempo recomendado para esta sesión',
            timestamp=datetime.now(),
            severidad='danger'
        )
    
    @classmethod
    def crear_alerta_inactividad(cls) -> 'AlertaSeguridad':
        """Crea una alerta de inactividad"""
        return cls(
            tipo='inactividad',
            mensaje='No se detecta actividad. ¿Estás bien?',
            timestamp=datetime.now(),
            severidad='warning'
        )

