"""
Servicio de Reportes - Generación de reportes en CSV y análisis de datos
"""
import csv
import io
from typing import List, Dict, Optional
from datetime import datetime, timedelta, date
from app.models.ejercicio import ResultadoEjercicio
from app.models.sesion import Sesion, EstadoSesion


class ReporteService:
    """Servicio para generar reportes y análisis"""
    
    def generar_reporte_csv_ejercicios(
        self,
        resultados: List[ResultadoEjercicio],
        paciente_nombre: str
    ) -> str:
        """Genera un reporte CSV de ejercicios"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Encabezados
        headers = [
            'Fecha',
            'Tipo Ejercicio',
            'Nivel',
            'Éxito',
            'Tiempo (s)',
            'Puntuación',
            'Precisión (%)',
            'Velocidad Promedio',
            'Rango Movimiento',
            'Tiempo Reacción (ms)',
            'Tasa Aciertos (%)',
            'Consistencia (%)',
            'Combo Máximo',
            'Aciertos',
            'Fallos'
        ]
        writer.writerow(headers)
        
        # Datos
        for resultado in resultados:
            row = [
                resultado.fecha,
                resultado.tipo_ejercicio,
                resultado.nivel,
                'Sí' if resultado.exito else 'No',
                resultado.tiempo_ejecucion or '',
                resultado.puntuacion or '',
                resultado.precision or '',
                resultado.velocidad_promedio or '',
                resultado.rango_movimiento or '',
                resultado.tiempo_reaccion_promedio or '',
                resultado.tasa_aciertos or '',
                resultado.consistencia or '',
                resultado.combo_maximo or '',
                resultado.aciertos or '',
                resultado.fallos or ''
            ]
            writer.writerow(row)
        
        # Agregar resumen
        writer.writerow([])
        writer.writerow(['RESUMEN DEL REPORTE'])
        writer.writerow(['Paciente:', paciente_nombre])
        writer.writerow(['Fecha de generación:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow(['Total de ejercicios:', len(resultados)])
        
        exitosos = sum(1 for r in resultados if r.exito)
        writer.writerow(['Ejercicios exitosos:', exitosos])
        writer.writerow(['Tasa de éxito:', f'{(exitosos/len(resultados)*100):.1f}%' if resultados else '0%'])
        
        return output.getvalue()
    
    def generar_reporte_csv_sesiones(
        self,
        sesiones: List[Sesion],
        paciente_nombre: str
    ) -> str:
        """Genera un reporte CSV de sesiones"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Encabezados
        headers = [
            'Fecha',
            'Tipo Terapia',
            'Duración (min)',
            'Estado',
            'Calentamiento',
            'Enfriamiento',
            'Alertas Descanso',
            'Pausas',
            'Nivel Fatiga (1-5)',
            'Nivel Dolor (0-10)',
            'Observaciones'
        ]
        writer.writerow(headers)
        
        # Datos
        for sesion in sesiones:
            row = [
                sesion.fecha_sesion.strftime('%Y-%m-%d %H:%M') if sesion.fecha_sesion else '',
                sesion.tipo_terapia.value,
                sesion.duracion_minutos,
                sesion.estado.value,
                'Sí' if sesion.calentamiento_completado else 'No',
                'Sí' if sesion.enfriamiento_completado else 'No',
                sesion.alertas_descanso,
                sesion.pausas_tomadas,
                sesion.nivel_fatiga or '',
                sesion.nivel_dolor or '',
                sesion.observaciones or ''
            ]
            writer.writerow(row)
        
        # Resumen
        writer.writerow([])
        writer.writerow(['RESUMEN DEL REPORTE'])
        writer.writerow(['Paciente:', paciente_nombre])
        writer.writerow(['Fecha de generación:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        
        sesiones_completadas = [s for s in sesiones if s.estado == EstadoSesion.COMPLETADA]
        writer.writerow(['Total sesiones:', len(sesiones)])
        writer.writerow(['Sesiones completadas:', len(sesiones_completadas)])
        
        if sesiones_completadas:
            tiempo_total = sum(s.duracion_minutos for s in sesiones_completadas)
            promedio = tiempo_total / len(sesiones_completadas)
            writer.writerow(['Tiempo total (min):', tiempo_total])
            writer.writerow(['Promedio duración (min):', f'{promedio:.1f}'])
        
        return output.getvalue()
    
    def generar_analisis_progreso(
        self,
        resultados: List[ResultadoEjercicio],
        periodo_dias: int = 30
    ) -> Dict:
        """Genera un análisis de progreso del paciente"""
        if not resultados:
            return {
                'sin_datos': True,
                'mensaje': 'No hay datos suficientes para análisis'
            }
        
        def _parse_fecha(fecha_str):
            """Parsea fecha ISO ignorando timezone para compatibilidad."""
            if not fecha_str:
                return None
            try:
                # Elimina timezone (+00:00, Z, etc.) antes de parsear
                limpia = fecha_str.split('+')[0].rstrip('Z').strip()
                return datetime.fromisoformat(limpia)
            except (ValueError, AttributeError):
                return None

        # Filtrar por período
        fecha_limite = datetime.now() - timedelta(days=periodo_dias)
        resultados_periodo = [
            r for r in resultados
            if _parse_fecha(r.fecha) and _parse_fecha(r.fecha) >= fecha_limite
        ]

        if not resultados_periodo:
            resultados_periodo = resultados  # Usar todos si no hay en el período

        # Análisis por tipo de ejercicio
        ejercicios_por_tipo = {}
        for resultado in resultados_periodo:
            tipo = resultado.tipo_ejercicio
            if tipo not in ejercicios_por_tipo:
                ejercicios_por_tipo[tipo] = []
            ejercicios_por_tipo[tipo].append(resultado)
        
        analisis_tipos = {}
        for tipo, resultados_tipo in ejercicios_por_tipo.items():
            exitosos = sum(1 for r in resultados_tipo if r.exito)
            tasa_exito = (exitosos / len(resultados_tipo)) * 100
            
            precisiones = [r.precision for r in resultados_tipo if r.precision]
            precision_promedio = sum(precisiones) / len(precisiones) if precisiones else None
            
            velocidades = [r.velocidad_promedio for r in resultados_tipo if r.velocidad_promedio]
            velocidad_promedio = sum(velocidades) / len(velocidades) if velocidades else None
            
            analisis_tipos[tipo] = {
                'total_intentos': len(resultados_tipo),
                'exitosos': exitosos,
                'tasa_exito': round(tasa_exito, 1),
                'precision_promedio': round(precision_promedio, 1) if precision_promedio else None,
                'velocidad_promedio': round(velocidad_promedio, 2) if velocidad_promedio else None
            }
        
        # Tendencia general (últimos 7 días vs anteriores)
        fecha_semana = datetime.now() - timedelta(days=7)
        ultima_semana = [r for r in resultados_periodo if _parse_fecha(r.fecha) and _parse_fecha(r.fecha) >= fecha_semana]
        semana_anterior = [r for r in resultados_periodo if _parse_fecha(r.fecha) and _parse_fecha(r.fecha) < fecha_semana]
        
        tendencia = 'estable'
        if ultima_semana and semana_anterior:
            tasa_reciente = sum(1 for r in ultima_semana if r.exito) / len(ultima_semana) * 100
            tasa_anterior = sum(1 for r in semana_anterior if r.exito) / len(semana_anterior) * 100
            
            if tasa_reciente > tasa_anterior + 5:
                tendencia = 'mejora'
            elif tasa_reciente < tasa_anterior - 5:
                tendencia = 'declive'
        
        # Métricas globales
        total_ejercicios = len(resultados_periodo)
        exitosos_total = sum(1 for r in resultados_periodo if r.exito)
        tasa_exito_global = (exitosos_total / total_ejercicios) * 100
        
        precisiones_todas = [r.precision for r in resultados_periodo if r.precision]
        precision_global = sum(precisiones_todas) / len(precisiones_todas) if precisiones_todas else None
        
        return {
            'periodo_dias': periodo_dias,
            'fecha_analisis': datetime.now().isoformat(),
            'metricas_globales': {
                'total_ejercicios': total_ejercicios,
                'ejercicios_exitosos': exitosos_total,
                'tasa_exito': round(tasa_exito_global, 1),
                'precision_promedio': round(precision_global, 1) if precision_global else None
            },
            'analisis_por_tipo': analisis_tipos,
            'tendencia': tendencia,
            'recomendaciones': self._generar_recomendaciones_progreso(
                tasa_exito_global, precision_global, tendencia
            )
        }
    
    def _generar_recomendaciones_progreso(
        self,
        tasa_exito: float,
        precision: Optional[float],
        tendencia: str
    ) -> List[str]:
        """Genera recomendaciones basadas en el progreso"""
        recomendaciones = []
        
        if tendencia == 'mejora':
            recomendaciones.append('¡Excelente progreso! Considera aumentar la dificultad.')
        elif tendencia == 'declive':
            recomendaciones.append('Se detecta una disminución en el rendimiento. Considera más descanso o reducir dificultad.')
        
        if tasa_exito < 50:
            recomendaciones.append('Tasa de éxito baja. Recomendamos disminuir la dificultad o aumentar el tiempo de práctica.')
        elif tasa_exito > 85:
            recomendaciones.append('Alto rendimiento. Puedes intentar ejercicios más desafiantes.')
        
        if precision and precision < 70:
            recomendaciones.append('La precisión puede mejorar. Enfócate en la calidad sobre la velocidad.')
        elif precision and precision > 90:
            recomendaciones.append('Excelente precisión. Intenta aumentar la velocidad gradualmente.')
        
        if not recomendaciones:
            recomendaciones.append('Continúa con tu práctica regular para mantener el progreso.')
        
        return recomendaciones
    
    def generar_comparativa_semanal(
        self,
        resultados: List[ResultadoEjercicio]
    ) -> Dict:
        """Genera una comparativa semanal de resultados"""
        if not resultados:
            return {'sin_datos': True}
        
        # Agrupar por semana
        resultados_por_semana = {}
        for resultado in resultados:
            if not resultado.fecha:
                continue
            try:
                fecha_limpia = resultado.fecha.split('+')[0].rstrip('Z').strip()
                fecha = datetime.fromisoformat(fecha_limpia).date()
            except (ValueError, AttributeError):
                continue
            semana = fecha.isocalendar()[1]  # Número de semana del año
            ano = fecha.year
            clave = f"{ano}-W{semana:02d}"
            
            if clave not in resultados_por_semana:
                resultados_por_semana[clave] = []
            resultados_por_semana[clave].append(resultado)
        
        # Analizar cada semana
        datos_semanales = []
        for semana, resultados_semana in sorted(resultados_por_semana.items()):
            exitosos = sum(1 for r in resultados_semana if r.exito)
            tasa_exito = (exitosos / len(resultados_semana)) * 100
            
            precisiones = [r.precision for r in resultados_semana if r.precision]
            precision_promedio = sum(precisiones) / len(precisiones) if precisiones else None
            
            datos_semanales.append({
                'semana': semana,
                'total_ejercicios': len(resultados_semana),
                'exitosos': exitosos,
                'tasa_exito': round(tasa_exito, 1),
                'precision_promedio': round(precision_promedio, 1) if precision_promedio else None
            })
        
        return {
            'datos_semanales': datos_semanales[-12:],  # Últimas 12 semanas
            'total_semanas': len(datos_semanales)
        }

