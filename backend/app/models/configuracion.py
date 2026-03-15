"""
Modelo de Configuración de Paciente - Accesibilidad y personalización
"""
from dataclasses import dataclass, asdict
from typing import Dict, Optional
from enum import Enum


class ModoAccesibilidad(Enum):
    """Modos de accesibilidad disponibles"""
    SENTADO = "sentado"
    PIE = "pie"
    AMBOS = "ambos"


class ManosHabilitadas(Enum):
    """Configuración de manos habilitadas"""
    IZQUIERDA = "izquierda"
    DERECHA = "derecha"
    AMBAS = "ambas"


class TamanoObjetivos(Enum):
    """Tamaño de objetivos en juego"""
    PEQUENO = "pequeno"
    MEDIANO = "mediano"
    GRANDE = "grande"


@dataclass
class CalibracionPaciente:
    """Clase de datos para calibración física del paciente"""
    paciente_id: int
    altura_cm: Optional[int] = None
    rango_movimiento_hombro: int = 180
    rango_movimiento_codo: int = 150
    rango_movimiento_muneca: int = 90
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CalibracionPaciente':
        """Crea desde un diccionario"""
        return cls(**data)
    
    def validar_rangos(self) -> bool:
        """Valida que los rangos estén dentro de límites fisiológicos"""
        return (
            0 <= self.rango_movimiento_hombro <= 180 and
            0 <= self.rango_movimiento_codo <= 150 and
            0 <= self.rango_movimiento_muneca <= 90
        )


@dataclass
class ConfiguracionAccesibilidad:
    """Clase de datos para configuración de accesibilidad"""
    paciente_id: int
    modo_accesibilidad: ModoAccesibilidad = ModoAccesibilidad.AMBOS
    manos_habilitadas: ManosHabilitadas = ManosHabilitadas.AMBAS
    velocidad_juego: float = 1.0
    tamano_objetivos: TamanoObjetivos = TamanoObjetivos.MEDIANO
    dificultad_adaptativa: bool = True
    controles_simplificados: bool = False
    texto_grande: bool = False
    alto_contraste: bool = False
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario"""
        data = asdict(self)
        data['modo_accesibilidad'] = self.modo_accesibilidad.value
        data['manos_habilitadas'] = self.manos_habilitadas.value
        data['tamano_objetivos'] = self.tamano_objetivos.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ConfiguracionAccesibilidad':
        """Crea desde un diccionario"""
        if isinstance(data.get('modo_accesibilidad'), str):
            data['modo_accesibilidad'] = ModoAccesibilidad(data['modo_accesibilidad'])
        if isinstance(data.get('manos_habilitadas'), str):
            data['manos_habilitadas'] = ManosHabilitadas(data['manos_habilitadas'])
        if isinstance(data.get('tamano_objetivos'), str):
            data['tamano_objetivos'] = TamanoObjetivos(data['tamano_objetivos'])
        return cls(**data)
    
    def obtener_multiplicador_velocidad(self) -> float:
        """Retorna el multiplicador de velocidad para aplicar al juego"""
        return self.velocidad_juego
    
    def obtener_escala_objetivos(self) -> float:
        """Retorna la escala de tamaño para objetivos"""
        escalas = {
            TamanoObjetivos.PEQUENO: 0.8,
            TamanoObjetivos.MEDIANO: 1.0,
            TamanoObjetivos.GRANDE: 1.5
        }
        return escalas.get(self.tamano_objetivos, 1.0)


@dataclass
class ConfiguracionSeguridad:
    """Clase de datos para configuración de seguridad"""
    paciente_id: int
    limite_tiempo_sesion: int = 30  # minutos
    intervalo_descanso: int = 10  # minutos
    duracion_descanso: int = 2  # minutos
    alerta_movimientos_bruscos: bool = True
    pausa_automatica_inactividad: bool = True
    tiempo_inactividad: int = 30  # segundos
    zona_juego_delimitada: bool = True
    sistema_antimareo: bool = True
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ConfiguracionSeguridad':
        """Crea desde un diccionario"""
        return cls(**data)


@dataclass
class ConfiguracionPaciente:
    """Clase que agrupa todas las configuraciones del paciente"""
    paciente_id: int
    calibracion: CalibracionPaciente
    accesibilidad: ConfiguracionAccesibilidad
    seguridad: ConfiguracionSeguridad
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario"""
        return {
            'paciente_id': self.paciente_id,
            'calibracion': self.calibracion.to_dict(),
            'accesibilidad': self.accesibilidad.to_dict(),
            'seguridad': self.seguridad.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ConfiguracionPaciente':
        """Crea desde un diccionario"""
        return cls(
            paciente_id=data['paciente_id'],
            calibracion=CalibracionPaciente.from_dict(data['calibracion']),
            accesibilidad=ConfiguracionAccesibilidad.from_dict(data['accesibilidad']),
            seguridad=ConfiguracionSeguridad.from_dict(data['seguridad'])
        )
    
    @classmethod
    def crear_default(cls, paciente_id: int) -> 'ConfiguracionPaciente':
        """Crea una configuración por defecto para un paciente"""
        return cls(
            paciente_id=paciente_id,
            calibracion=CalibracionPaciente(paciente_id=paciente_id),
            accesibilidad=ConfiguracionAccesibilidad(paciente_id=paciente_id),
            seguridad=ConfiguracionSeguridad(paciente_id=paciente_id)
        )

