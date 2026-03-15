"""
Controlador de Gamificación - Endpoints para sistema de puntos y logros
"""
from flask import Blueprint, request, jsonify, session
from app.services.gamificacion_service import GamificacionService

gamificacion_bp = Blueprint('gamificacion', __name__)
gamif_service = GamificacionService()


def _get_paciente_id():
    """Obtiene el ID del paciente de la sesión activa. Retorna None si no hay sesión."""
    paciente_data = session.get('paciente')
    if not paciente_data:
        return None
    return paciente_data.get('id')


@gamificacion_bp.route('/gamificacion', methods=['GET'])
def obtener_gamificacion():
    """Obtiene el estado de gamificación del paciente"""
    paciente_id = _get_paciente_id()
    if not paciente_id:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401

    gamificacion = gamif_service.inicializar_gamificacion(paciente_id)
    resumen = gamif_service.obtener_resumen_gamificacion(gamificacion)

    return jsonify({
        'success': True,
        'gamificacion': resumen
    })


@gamificacion_bp.route('/gamificacion/logros', methods=['GET'])
def obtener_logros():
    """Obtiene todos los logros disponibles"""
    logros = gamif_service.obtener_todos_logros()

    return jsonify({
        'success': True,
        'logros': logros
    })


@gamificacion_bp.route('/gamificacion/logros/paciente', methods=['GET'])
def obtener_logros_paciente():
    """Obtiene los logros del paciente con su progreso"""
    paciente_id = _get_paciente_id()
    if not paciente_id:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401

    return jsonify({
        'success': True,
        'logros': [],
        'completados': 0,
        'total': len(gamif_service.obtener_todos_logros())
    })


@gamificacion_bp.route('/gamificacion/objetivo-diario', methods=['GET'])
def obtener_objetivo_diario():
    """Obtiene el objetivo diario del paciente"""
    paciente_id = _get_paciente_id()
    if not paciente_id:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401

    objetivo = gamif_service.crear_objetivo_diario(paciente_id)

    return jsonify({
        'success': True,
        'objetivo': objetivo.to_dict(),
        'progreso_sesiones': objetivo.progreso_sesiones(),
        'progreso_tiempo': objetivo.progreso_tiempo()
    })


@gamificacion_bp.route('/gamificacion/ranking', methods=['GET'])
def obtener_ranking():
    """Obtiene el ranking de pacientes"""
    return jsonify({
        'success': True,
        'ranking': []
    })

