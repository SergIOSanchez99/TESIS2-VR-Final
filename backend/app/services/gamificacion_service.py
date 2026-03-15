"""
Servicio de Gamificación - Lógica de negocio para puntos, logros y recompensas
"""
from typing import List, Dict, Optional
from datetime import date, datetime
from app.models.gamificacion import (
    GamificacionPaciente, Logro, LogroPaciente, ObjetivoDiario,
    TipoLogro, LOGROS_PREDEFINIDOS
)


class GamificacionService:
    """Servicio para gestionar la gamificación"""
    
    def __init__(self):
        self.logros_disponibles = {logro.codigo: logro for logro in LOGROS_PREDEFINIDOS}
    
    def inicializar_gamificacion(self, paciente_id: int) -> GamificacionPaciente:
        """Inicializa la gamificación para un paciente nuevo"""
        return GamificacionPaciente(
            paciente_id=paciente_id,
            puntos_totales=0,
            nivel_actual=1,
            experiencia_actual=0,
            experiencia_siguiente_nivel=100,
            racha_dias=0,
            ultima_actividad=None,
            avatar_seleccionado='default'
        )
    
    def registrar_actividad(self, gamificacion: GamificacionPaciente) -> Dict:
        """
        Registra una actividad y actualiza racha
        
        Returns:
            Dict con información sobre cambios (subió nivel, logros, etc.)
        """
        gamificacion.actualizar_racha()
        
        # Otorgar puntos base por completar actividad
        puntos_base = 10
        exp_base = 20
        
        gamificacion.agregar_puntos(puntos_base)
        subio_nivel = gamificacion.agregar_experiencia(exp_base)
        
        return {
            'puntos_ganados': puntos_base,
            'experiencia_ganada': exp_base,
            'subio_nivel': subio_nivel,
            'nuevo_nivel': gamificacion.nivel_actual if subio_nivel else None,
            'racha_actual': gamificacion.racha_dias
        }
    
    def registrar_ejercicio_completado(
        self,
        gamificacion: GamificacionPaciente,
        duracion_segundos: int,
        exito: bool,
        precision: Optional[float] = None
    ) -> Dict:
        """
        Registra un ejercicio completado y otorga recompensas
        
        Returns:
            Dict con información sobre recompensas
        """
        resultado = self.registrar_actividad(gamificacion)
        
        # Bonus por éxito
        if exito:
            bonus_exito = 25
            gamificacion.agregar_puntos(bonus_exito)
            resultado['puntos_ganados'] += bonus_exito
            resultado['bonus_exito'] = True
        
        # Bonus por precisión (base 80 = umbral mínimo para el bonus)
        if precision and precision >= 80:
            bonus_precision = int((precision - 80) * 2)
            gamificacion.agregar_puntos(bonus_precision)
            resultado['puntos_ganados'] += bonus_precision
            resultado['bonus_precision'] = bonus_precision
        
        # Bonus por velocidad
        if duracion_segundos < 60:
            bonus_velocidad = 15
            gamificacion.agregar_puntos(bonus_velocidad)
            gamificacion.agregar_experiencia(10)
            resultado['puntos_ganados'] += bonus_velocidad
            resultado['experiencia_ganada'] += 10
            resultado['bonus_velocidad'] = True
        
        return resultado
    
    def verificar_logros(
        self,
        paciente_id: int,
        sesiones_completadas: int,
        precision_maxima: float,
        racha_dias: int,
        duracion_ejercicio: Optional[int] = None,
        logros_paciente: Optional[List[LogroPaciente]] = None
    ) -> List[Logro]:
        """
        Verifica qué logros se han desbloqueado
        
        Returns:
            Lista de logros nuevos desbloqueados
        """
        logros_nuevos = []
        logros_completados = set()
        
        if logros_paciente:
            logros_completados = {lp.logro_id for lp in logros_paciente if lp.completado}
        
        for codigo, logro in self.logros_disponibles.items():
            # Si ya está completado, saltar
            if logro.id in logros_completados:
                continue
            
            cumple_requisito = False
            
            if logro.tipo == TipoLogro.SESIONES:
                cumple_requisito = sesiones_completadas >= logro.requisito_valor
            
            elif logro.tipo == TipoLogro.PRECISION:
                cumple_requisito = precision_maxima >= logro.requisito_valor
            
            elif logro.tipo == TipoLogro.RACHA:
                cumple_requisito = racha_dias >= logro.requisito_valor
            
            elif logro.tipo == TipoLogro.ESPECIAL:
                if codigo == "velocista" and duracion_ejercicio:
                    cumple_requisito = duracion_ejercicio <= logro.requisito_valor
            
            if cumple_requisito:
                logros_nuevos.append(logro)
        
        return logros_nuevos
    
    def otorgar_logro(
        self,
        gamificacion: GamificacionPaciente,
        logro: Logro
    ) -> Dict:
        """
        Otorga un logro y sus recompensas
        
        Returns:
            Dict con información del logro otorgado
        """
        gamificacion.agregar_puntos(logro.puntos_recompensa)
        gamificacion.agregar_experiencia(logro.puntos_recompensa)
        
        return {
            'logro': logro.to_dict(),
            'puntos_ganados': logro.puntos_recompensa,
            'experiencia_ganada': logro.puntos_recompensa
        }
    
    def crear_objetivo_diario(self, paciente_id: int, fecha: Optional[date] = None) -> ObjetivoDiario:
        """Crea un objetivo diario para el paciente"""
        if not fecha:
            fecha = date.today()
        
        return ObjetivoDiario(
            paciente_id=paciente_id,
            fecha=fecha,
            objetivo_sesiones=1,
            sesiones_completadas=0,
            objetivo_tiempo_minutos=15,
            tiempo_completado_minutos=0,
            completado=False
        )
    
    def verificar_objetivo_diario(
        self,
        objetivo: ObjetivoDiario,
        gamificacion: GamificacionPaciente
    ) -> Optional[Dict]:
        """
        Verifica si se completó el objetivo diario y otorga recompensas
        
        Returns:
            Dict con recompensas si se completó, None si no
        """
        if objetivo.completado:
            # Bonus por completar objetivo diario
            bonus_objetivo = 50
            gamificacion.agregar_puntos(bonus_objetivo)
            gamificacion.agregar_experiencia(30)
            
            return {
                'objetivo_completado': True,
                'puntos_ganados': bonus_objetivo,
                'experiencia_ganada': 30
            }
        
        return None
    
    def obtener_resumen_gamificacion(self, gamificacion: GamificacionPaciente) -> Dict:
        """Obtiene un resumen de la gamificación del paciente"""
        exp_siguiente = gamificacion.experiencia_siguiente_nivel or 1
        progreso_nivel = (gamificacion.experiencia_actual / exp_siguiente) * 100
        
        return {
            'puntos_totales': gamificacion.puntos_totales,
            'nivel_actual': gamificacion.nivel_actual,
            'experiencia_actual': gamificacion.experiencia_actual,
            'experiencia_siguiente_nivel': gamificacion.experiencia_siguiente_nivel,
            'progreso_nivel': round(progreso_nivel, 1),
            'racha_dias': gamificacion.racha_dias,
            'ultima_actividad': gamificacion.ultima_actividad.isoformat() if gamificacion.ultima_actividad else None,
            'avatar': gamificacion.avatar_seleccionado
        }
    
    def obtener_todos_logros(self) -> List[Dict]:
        """Obtiene todos los logros disponibles"""
        return [logro.to_dict() for logro in LOGROS_PREDEFINIDOS]
    
    def calcular_ranking_semanal(self, gamificaciones: List[GamificacionPaciente]) -> List[Dict]:
        """
        Calcula el ranking de pacientes por puntos
        
        Returns:
            Lista ordenada de pacientes con sus puntos
        """
        ranking = sorted(
            gamificaciones,
            key=lambda g: g.puntos_totales,
            reverse=True
        )
        
        return [
            {
                'posicion': i + 1,
                'paciente_id': g.paciente_id,
                'puntos': g.puntos_totales,
                'nivel': g.nivel_actual,
                'avatar': g.avatar_seleccionado
            }
            for i, g in enumerate(ranking[:10])  # Top 10
        ]

