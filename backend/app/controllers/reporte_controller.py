"""
Controlador de Reportes - Endpoints para generación y descarga de reportes
"""
from flask import Blueprint, request, jsonify, session, make_response
from app.services.reporte_service import ReporteService
from app.services.paciente_service import PacienteService
from app.services.ejercicio_service import EjercicioService
from datetime import datetime

reporte_bp = Blueprint('reporte', __name__)
reporte_service = ReporteService()
paciente_service = PacienteService()
ejercicio_service = EjercicioService()


def _get_paciente_id():
    """Obtiene el ID del paciente de la sesión activa. Retorna None si no hay sesión."""
    paciente_data = session.get('paciente')
    if not paciente_data:
        return None
    return paciente_data.get('id')


@reporte_bp.route('/reporte/ejercicios/csv', methods=['GET'])
def descargar_reporte_ejercicios_csv():
    """Descarga un reporte CSV de ejercicios del paciente"""
    paciente_id = _get_paciente_id()
    if not paciente_id:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401

    paciente = paciente_service.obtener_paciente(str(paciente_id))
    paciente_nombre = paciente.nombre if paciente else "Paciente"

    historial = ejercicio_service.obtener_historial_paciente(str(paciente_id))

    csv_content = reporte_service.generar_reporte_csv_ejercicios(historial, paciente_nombre)

    response = make_response(csv_content)
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = (
        f'attachment; filename=reporte_ejercicios_{datetime.now().strftime("%Y%m%d")}.csv'
    )

    return response


@reporte_bp.route('/reporte/sesiones/csv', methods=['GET'])
def descargar_reporte_sesiones_csv():
    """Descarga un reporte CSV de sesiones del paciente"""
    paciente_id = _get_paciente_id()
    if not paciente_id:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401

    return jsonify({
        'success': False,
        'error': 'Funcionalidad en desarrollo'
    }), 501


@reporte_bp.route('/reporte/progreso', methods=['GET'])
def obtener_analisis_progreso():
    """Obtiene un análisis de progreso del paciente"""
    paciente_id = _get_paciente_id()
    if not paciente_id:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401

    periodo = request.args.get('periodo', 30, type=int)

    historial = ejercicio_service.obtener_historial_paciente(str(paciente_id))
    analisis = reporte_service.generar_analisis_progreso(historial, periodo)

    return jsonify({
        'success': True,
        'analisis': analisis
    })


@reporte_bp.route('/reporte/comparativa-semanal', methods=['GET'])
def obtener_comparativa_semanal():
    """Obtiene una comparativa semanal de resultados"""
    paciente_id = _get_paciente_id()
    if not paciente_id:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401

    historial = ejercicio_service.obtener_historial_paciente(str(paciente_id))
    comparativa = reporte_service.generar_comparativa_semanal(historial)

    return jsonify({
        'success': True,
        'comparativa': comparativa
    })
