"""
Servicio de Sesiones - Lógica de negocio para gestión de sesiones de terapia
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.models.sesion import (
    Sesion, EstadoSesion, TipoTerapia, AlertaSeguridad,
    EJERCICIOS_CALENTAMIENTO, EJERCICIOS_ENFRIAMIENTO
)
from app.models.configuracion import ConfiguracionSeguridad


class SesionService:
    """Servicio para gestionar sesiones de terapia"""
    
    def crear_sesion(
        self,
        paciente_id: int,
        tipo_terapia: TipoTerapia,
        config_seguridad: Optional[ConfiguracionSeguridad] = None
    ) -> Sesion:
        """Crea una nueva sesión de terapia"""
        sesion = Sesion(
            paciente_id=paciente_id,
            tipo_terapia=tipo_terapia
        )
        
        return sesion
    
    def iniciar_sesion(self, sesion: Sesion) -> Dict:
        """Inicia una sesión con advertencias de seguridad"""
        sesion.iniciar()
        
        return {
            'sesion_iniciada': True,
            'estado': sesion.estado.value,
            'advertencias_seguridad': [
                'Asegúrate de tener suficiente espacio alrededor',
                'Si sientes mareo, pausa inmediatamente la sesión',
                'Realiza los ejercicios de calentamiento antes de comenzar',
                'Si sientes dolor, detén el ejercicio'
            ],
            'ejercicios_calentamiento': [e.to_dict() for e in EJERCICIOS_CALENTAMIENTO]
        }
    
    def completar_calentamiento(self, sesion: Sesion) -> Dict:
        """Marca el calentamiento como completado"""
        sesion.completar_calentamiento()
        
        return {
            'calentamiento_completado': True,
            'estado': sesion.estado.value,
            'mensaje': '¡Excelente! Ahora puedes comenzar con los ejercicios'
        }
    
    def verificar_alertas_seguridad(
        self,
        sesion: Sesion,
        config_seguridad: ConfiguracionSeguridad
    ) -> List[AlertaSeguridad]:
        """Verifica y genera alertas de seguridad si es necesario"""
        alertas = []
        
        # Verificar descanso
        if sesion.requiere_descanso(config_seguridad.intervalo_descanso):
            alerta = AlertaSeguridad.crear_alerta_descanso()
            alertas.append(alerta)
            sesion.registrar_alerta_descanso()
        
        # Verificar límite de tiempo
        if sesion.excede_limite_tiempo(config_seguridad.limite_tiempo_sesion):
            alerta = AlertaSeguridad.crear_alerta_limite_tiempo()
            alertas.append(alerta)
        
        return alertas
    
    def pausar_sesion(self, sesion: Sesion) -> Dict:
        """Pausa la sesión"""
        sesion.pausar()
        
        return {
            'sesion_pausada': True,
            'estado': sesion.estado.value,
            'tiempo_transcurrido': sesion.tiempo_transcurrido(),
            'mensaje': 'Toma un descanso. Presiona continuar cuando estés listo'
        }
    
    def reanudar_sesion(self, sesion: Sesion) -> Dict:
        """Reanuda la sesión"""
        sesion.reanudar()
        
        return {
            'sesion_reanudada': True,
            'estado': sesion.estado.value,
            'mensaje': '¡Continuemos!'
        }
    
    def iniciar_enfriamiento(self, sesion: Sesion) -> Dict:
        """Inicia la fase de enfriamiento"""
        sesion.iniciar_enfriamiento()
        
        return {
            'enfriamiento_iniciado': True,
            'estado': sesion.estado.value,
            'ejercicios_enfriamiento': [e.to_dict() for e in EJERCICIOS_ENFRIAMIENTO],
            'mensaje': 'Excelente trabajo. Realiza estos ejercicios de enfriamiento'
        }
    
    def completar_enfriamiento(self, sesion: Sesion) -> Dict:
        """Completa el enfriamiento y finaliza la sesión"""
        sesion.completar_enfriamiento()
        
        return {
            'enfriamiento_completado': True,
            'sesion_finalizada': True,
            'duracion_total': sesion.duracion_minutos,
            'mensaje': '¡Sesión completada! Por favor responde la encuesta'
        }
    
    def registrar_encuesta_post_sesion(
        self,
        sesion: Sesion,
        nivel_fatiga: int,
        nivel_dolor: int,
        observaciones: Optional[str] = None
    ) -> Dict:
        """Registra la encuesta post-sesión"""
        sesion.registrar_encuesta(nivel_fatiga, nivel_dolor, observaciones)
        
        # Generar recomendaciones basadas en la encuesta
        recomendaciones = []
        
        if nivel_fatiga >= 4:
            recomendaciones.append('Descansa más antes de la próxima sesión')
            recomendaciones.append('Considera reducir la duración de las sesiones')
        
        if nivel_dolor >= 5:
            recomendaciones.append('Consulta con tu terapeuta sobre el dolor')
            recomendaciones.append('Reduce la intensidad de los ejercicios')
        
        if nivel_fatiga <= 2 and nivel_dolor <= 2:
            recomendaciones.append('¡Excelente! Puedes aumentar gradualmente la dificultad')
        
        return {
            'encuesta_registrada': True,
            'nivel_fatiga': nivel_fatiga,
            'nivel_dolor': nivel_dolor,
            'recomendaciones': recomendaciones
        }
    
    def cancelar_sesion(self, sesion: Sesion, motivo: Optional[str] = None) -> Dict:
        """Cancela la sesión"""
        if motivo:
            sesion.observaciones = f"Cancelada: {motivo}"
        sesion.cancelar()
        
        return {
            'sesion_cancelada': True,
            'mensaje': 'Sesión cancelada. Descansa y vuelve cuando te sientas mejor'
        }
    
    def obtener_resumen_sesion(self, sesion: Sesion) -> Dict:
        """Obtiene un resumen completo de la sesión"""
        return {
            'id': sesion.id,
            'paciente_id': sesion.paciente_id,
            'tipo_terapia': sesion.tipo_terapia.value,
            'duracion_minutos': sesion.duracion_minutos,
            'fecha_inicio': sesion.fecha_inicio.isoformat() if sesion.fecha_inicio else None,
            'fecha_fin': sesion.fecha_fin.isoformat() if sesion.fecha_fin else None,
            'estado': sesion.estado.value,
            'calentamiento_completado': sesion.calentamiento_completado,
            'enfriamiento_completado': sesion.enfriamiento_completado,
            'alertas_descanso': sesion.alertas_descanso,
            'pausas_tomadas': sesion.pausas_tomadas,
            'nivel_fatiga': sesion.nivel_fatiga,
            'nivel_dolor': sesion.nivel_dolor,
            'observaciones': sesion.observaciones
        }
    
    def obtener_estadisticas_sesiones(self, sesiones: List[Sesion]) -> Dict:
        """Obtiene estadísticas de un conjunto de sesiones"""
        if not sesiones:
            return {
                'total_sesiones': 0,
                'tiempo_total_minutos': 0,
                'promedio_duracion': 0,
                'promedio_fatiga': 0,
                'promedio_dolor': 0,
                'sesiones_con_descansos': 0
            }
        
        sesiones_completadas = [s for s in sesiones if s.estado == EstadoSesion.COMPLETADA]
        
        total_tiempo = sum(s.duracion_minutos for s in sesiones_completadas)
        promedio_duracion = total_tiempo / len(sesiones_completadas) if sesiones_completadas else 0
        
        sesiones_con_fatiga = [s for s in sesiones_completadas if s.nivel_fatiga is not None]
        promedio_fatiga = (
            sum(s.nivel_fatiga for s in sesiones_con_fatiga) / len(sesiones_con_fatiga)
            if sesiones_con_fatiga else 0
        )
        
        sesiones_con_dolor = [s for s in sesiones_completadas if s.nivel_dolor is not None]
        promedio_dolor = (
            sum(s.nivel_dolor for s in sesiones_con_dolor) / len(sesiones_con_dolor)
            if sesiones_con_dolor else 0
        )
        
        sesiones_con_descansos = sum(1 for s in sesiones_completadas if s.alertas_descanso > 0)
        
        return {
            'total_sesiones': len(sesiones),
            'sesiones_completadas': len(sesiones_completadas),
            'tiempo_total_minutos': total_tiempo,
            'promedio_duracion': round(promedio_duracion, 1),
            'promedio_fatiga': round(promedio_fatiga, 1),
            'promedio_dolor': round(promedio_dolor, 1),
            'sesiones_con_descansos': sesiones_con_descansos
        }

