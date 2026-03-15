"""
Servicio de Configuración - Lógica de negocio para configuración de pacientes
"""
from typing import Dict, Optional
from app.models.configuracion import (
    ConfiguracionPaciente, CalibracionPaciente,
    ConfiguracionAccesibilidad, ConfiguracionSeguridad,
    ModoAccesibilidad, ManosHabilitadas, TamanoObjetivos
)


class ConfiguracionService:
    """Servicio para gestionar configuraciones de pacientes"""
    
    def crear_configuracion_default(self, paciente_id: int) -> ConfiguracionPaciente:
        """Crea una configuración por defecto para un paciente nuevo"""
        return ConfiguracionPaciente.crear_default(paciente_id)
    
    def actualizar_calibracion(
        self,
        config: ConfiguracionPaciente,
        altura_cm: Optional[int] = None,
        rango_hombro: Optional[int] = None,
        rango_codo: Optional[int] = None,
        rango_muneca: Optional[int] = None
    ) -> Dict:
        """Actualiza la calibración física del paciente"""
        if altura_cm is not None:
            config.calibracion.altura_cm = altura_cm
        
        if rango_hombro is not None:
            config.calibracion.rango_movimiento_hombro = min(180, max(0, rango_hombro))
        
        if rango_codo is not None:
            config.calibracion.rango_movimiento_codo = min(150, max(0, rango_codo))
        
        if rango_muneca is not None:
            config.calibracion.rango_movimiento_muneca = min(90, max(0, rango_muneca))
        
        if not config.calibracion.validar_rangos():
            return {
                'error': 'Rangos de movimiento fuera de límites fisiológicos',
                'valido': False
            }
        
        return {
            'calibracion_actualizada': True,
            'calibracion': config.calibracion.to_dict(),
            'valido': True
        }
    
    def actualizar_accesibilidad(
        self,
        config: ConfiguracionPaciente,
        modo: Optional[str] = None,
        manos: Optional[str] = None,
        velocidad: Optional[float] = None,
        tamano: Optional[str] = None,
        dificultad_adaptativa: Optional[bool] = None,
        controles_simplificados: Optional[bool] = None,
        texto_grande: Optional[bool] = None,
        alto_contraste: Optional[bool] = None
    ) -> Dict:
        """Actualiza la configuración de accesibilidad"""
        acc = config.accesibilidad
        
        if modo:
            try:
                acc.modo_accesibilidad = ModoAccesibilidad(modo)
            except ValueError:
                return {'error': f'Modo inválido: {modo}', 'valido': False}
        
        if manos:
            try:
                acc.manos_habilitadas = ManosHabilitadas(manos)
            except ValueError:
                return {'error': f'Configuración de manos inválida: {manos}', 'valido': False}
        
        if velocidad is not None:
            # Limitar velocidad entre 0.5x y 2.0x
            acc.velocidad_juego = min(2.0, max(0.5, velocidad))
        
        if tamano:
            try:
                acc.tamano_objetivos = TamanoObjetivos(tamano)
            except ValueError:
                return {'error': f'Tamaño inválido: {tamano}', 'valido': False}
        
        if dificultad_adaptativa is not None:
            acc.dificultad_adaptativa = dificultad_adaptativa
        
        if controles_simplificados is not None:
            acc.controles_simplificados = controles_simplificados
        
        if texto_grande is not None:
            acc.texto_grande = texto_grande
        
        if alto_contraste is not None:
            acc.alto_contraste = alto_contraste
        
        return {
            'accesibilidad_actualizada': True,
            'accesibilidad': acc.to_dict(),
            'valido': True
        }
    
    def actualizar_seguridad(
        self,
        config: ConfiguracionPaciente,
        limite_tiempo: Optional[int] = None,
        intervalo_descanso: Optional[int] = None,
        duracion_descanso: Optional[int] = None,
        alerta_movimientos: Optional[bool] = None,
        pausa_auto: Optional[bool] = None,
        tiempo_inactividad: Optional[int] = None,
        zona_delimitada: Optional[bool] = None,
        antimareo: Optional[bool] = None
    ) -> Dict:
        """Actualiza la configuración de seguridad"""
        seg = config.seguridad
        
        if limite_tiempo is not None:
            seg.limite_tiempo_sesion = max(5, min(60, limite_tiempo))
        
        if intervalo_descanso is not None:
            seg.intervalo_descanso = max(5, min(30, intervalo_descanso))
        
        if duracion_descanso is not None:
            seg.duracion_descanso = max(1, min(10, duracion_descanso))
        
        if alerta_movimientos is not None:
            seg.alerta_movimientos_bruscos = alerta_movimientos
        
        if pausa_auto is not None:
            seg.pausa_automatica_inactividad = pausa_auto
        
        if tiempo_inactividad is not None:
            seg.tiempo_inactividad = max(10, min(120, tiempo_inactividad))
        
        if zona_delimitada is not None:
            seg.zona_juego_delimitada = zona_delimitada
        
        if antimareo is not None:
            seg.sistema_antimareo = antimareo
        
        return {
            'seguridad_actualizada': True,
            'seguridad': seg.to_dict(),
            'valido': True
        }
    
    def obtener_configuracion_completa(self, config: ConfiguracionPaciente) -> Dict:
        """Obtiene la configuración completa del paciente"""
        return config.to_dict()
    
    def aplicar_preset_accesibilidad(
        self,
        config: ConfiguracionPaciente,
        preset: str
    ) -> Dict:
        """Aplica un preset de configuración de accesibilidad"""
        presets = {
            'principiante': {
                'velocidad': 0.7,
                'tamano': 'grande',
                'dificultad_adaptativa': True,
                'controles_simplificados': True,
                'texto_grande': True
            },
            'intermedio': {
                'velocidad': 1.0,
                'tamano': 'mediano',
                'dificultad_adaptativa': True,
                'controles_simplificados': False,
                'texto_grande': False
            },
            'avanzado': {
                'velocidad': 1.3,
                'tamano': 'pequeno',
                'dificultad_adaptativa': False,
                'controles_simplificados': False,
                'texto_grande': False
            },
            'movilidad_limitada': {
                'velocidad': 0.6,
                'tamano': 'grande',
                'modo': 'sentado',
                'dificultad_adaptativa': True,
                'controles_simplificados': True
            },
            'vision_reducida': {
                'tamano': 'grande',
                'texto_grande': True,
                'alto_contraste': True,
                'controles_simplificados': True
            }
        }
        
        if preset not in presets:
            return {
                'error': f'Preset no encontrado: {preset}',
                'valido': False,
                'presets_disponibles': list(presets.keys())
            }
        
        preset_config = presets[preset]
        resultado = self.actualizar_accesibilidad(config, **preset_config)
        
        if resultado.get('valido'):
            resultado['preset_aplicado'] = preset
        
        return resultado
    
    def obtener_recomendaciones(self, config: ConfiguracionPaciente) -> Dict:
        """Genera recomendaciones basadas en la configuración actual"""
        recomendaciones = []
        
        cal = config.calibracion
        acc = config.accesibilidad
        
        # Recomendaciones basadas en rango de movimiento
        if cal.rango_movimiento_hombro < 90:
            recomendaciones.append({
                'tipo': 'calibracion',
                'mensaje': 'Rango de movimiento del hombro limitado. Considera ejercicios de movilidad.',
                'prioridad': 'alta'
            })
            if acc.tamano_objetivos != TamanoObjetivos.GRANDE:
                recomendaciones.append({
                    'tipo': 'accesibilidad',
                    'mensaje': 'Recomendamos usar objetivos grandes dada tu movilidad.',
                    'accion': 'Cambiar a tamaño grande',
                    'prioridad': 'media'
                })
        
        # Recomendaciones de velocidad
        if acc.velocidad_juego > 1.2 and not acc.dificultad_adaptativa:
            recomendaciones.append({
                'tipo': 'accesibilidad',
                'mensaje': 'Velocidad alta sin dificultad adaptativa. Actívala para mejor experiencia.',
                'prioridad': 'baja'
            })
        
        # Recomendaciones de seguridad
        seg = config.seguridad
        if seg.limite_tiempo_sesion > 30:
            recomendaciones.append({
                'tipo': 'seguridad',
                'mensaje': 'Límite de sesión alto. Para principiantes se recomiendan sesiones de 15-20 minutos.',
                'prioridad': 'media'
            })
        
        return {
            'recomendaciones': recomendaciones,
            'total': len(recomendaciones)
        }

