"""
Controlador de Sesiones - Endpoints para gestión de sesiones de terapia
"""
from flask import Blueprint, request, jsonify, session
from app.services.sesion_service import SesionService
from app.services.configuracion_service import ConfiguracionService
from app.models.sesion import TipoTerapia

sesion_bp = Blueprint('sesion', __name__)
sesion_service = SesionService()
config_service = ConfiguracionService()


def _get_paciente_id():
    """Obtiene el ID del paciente de la sesión activa. Retorna None si no hay sesión."""
    paciente_data = session.get('paciente')
    if not paciente_data:
        return None
    return paciente_data.get('id')


@sesion_bp.route('/sesion/iniciar', methods=['POST'])
def iniciar_sesion():
    """Inicia una nueva sesión de terapia"""
    paciente_id = _get_paciente_id()
    if not paciente_id:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401
    data = request.get_json()
    
    tipo_terapia_str = data.get('tipo_terapia', 'rehabilitacion')
    try:
        tipo_terapia = TipoTerapia(tipo_terapia_str)
    except ValueError:
        return jsonify({'success': False, 'error': 'Tipo de terapia inválido'}), 400
    
    # Crear y iniciar sesión
    nueva_sesion = sesion_service.crear_sesion(paciente_id, tipo_terapia)
    resultado = sesion_service.iniciar_sesion(nueva_sesion)
    
    # TODO: Guardar en BD
    session['sesion_activa_id'] = nueva_sesion.id
    
    return jsonify({
        'success': True,
        **resultado
    })


@sesion_bp.route('/sesion/calentamiento/completar', methods=['POST'])
def completar_calentamiento():
    """Marca el calentamiento como completado"""
    if not _get_paciente_id() or 'sesion_activa_id' not in session:
        return jsonify({'success': False, 'error': 'No hay sesión activa'}), 400
    
    # TODO: Obtener sesión de BD
    # Por ahora simular
    
    return jsonify({
        'success': True,
        'calentamiento_completado': True,
        'mensaje': '¡Excelente! Ahora puedes comenzar con los ejercicios'
    })


@sesion_bp.route('/sesion/pausar', methods=['POST'])
def pausar_sesion():
    """Pausa la sesión activa"""
    if 'sesion_activa_id' not in session:
        return jsonify({'success': False, 'error': 'No hay sesión activa'}), 400
    
    # TODO: Obtener y pausar sesión en BD
    
    return jsonify({
        'success': True,
        'sesion_pausada': True,
        'mensaje': 'Toma un descanso. Presiona continuar cuando estés listo'
    })


@sesion_bp.route('/sesion/reanudar', methods=['POST'])
def reanudar_sesion():
    """Reanuda la sesión activa"""
    if 'sesion_activa_id' not in session:
        return jsonify({'success': False, 'error': 'No hay sesión activa'}), 400
    
    # TODO: Obtener y reanudar sesión en BD
    
    return jsonify({
        'success': True,
        'sesion_reanudada': True,
        'mensaje': '¡Continuemos!'
    })


@sesion_bp.route('/sesion/enfriamiento/iniciar', methods=['POST'])
def iniciar_enfriamiento():
    """Inicia la fase de enfriamiento"""
    if 'sesion_activa_id' not in session:
        return jsonify({'success': False, 'error': 'No hay sesión activa'}), 400
    
    # TODO: Obtener sesión de BD
    
    from app.models.sesion import EJERCICIOS_ENFRIAMIENTO
    
    return jsonify({
        'success': True,
        'enfriamiento_iniciado': True,
        'ejercicios_enfriamiento': [e.to_dict() for e in EJERCICIOS_ENFRIAMIENTO],
        'mensaje': 'Excelente trabajo. Realiza estos ejercicios de enfriamiento'
    })


@sesion_bp.route('/sesion/enfriamiento/completar', methods=['POST'])
def completar_enfriamiento():
    """Completa el enfriamiento y finaliza la sesión"""
    if 'sesion_activa_id' not in session:
        return jsonify({'success': False, 'error': 'No hay sesión activa'}), 400
    
    # TODO: Obtener sesión, completar enfriamiento y guardar en BD
    session.pop('sesion_activa_id', None)
    
    return jsonify({
        'success': True,
        'enfriamiento_completado': True,
        'sesion_finalizada': True,
        'mensaje': '¡Sesión completada! Por favor responde la encuesta'
    })


@sesion_bp.route('/sesion/encuesta', methods=['POST'])
def registrar_encuesta():
    """Registra la encuesta post-sesión"""
    if not _get_paciente_id():
        return jsonify({'success': False, 'error': 'No autenticado'}), 401
    
    data = request.get_json()
    
    nivel_fatiga = data.get('nivel_fatiga')
    nivel_dolor = data.get('nivel_dolor')
    observaciones = data.get('observaciones')
    
    if nivel_fatiga is None or nivel_dolor is None:
        return jsonify({'success': False, 'error': 'Datos incompletos'}), 400
    
    # TODO: Registrar encuesta en BD
    
    # Generar recomendaciones
    recomendaciones = []
    if nivel_fatiga >= 4:
        recomendaciones.append('Descansa más antes de la próxima sesión')
        recomendaciones.append('Considera reducir la duración de las sesiones')
    
    if nivel_dolor >= 5:
        recomendaciones.append('Consulta con tu terapeuta sobre el dolor')
        recomendaciones.append('Reduce la intensidad de los ejercicios')
    
    if nivel_fatiga <= 2 and nivel_dolor <= 2:
        recomendaciones.append('¡Excelente! Puedes aumentar gradualmente la dificultad')
    
    return jsonify({
        'success': True,
        'encuesta_registrada': True,
        'recomendaciones': recomendaciones
    })


@sesion_bp.route('/sesion/alertas', methods=['GET'])
def verificar_alertas():
    """Verifica y devuelve alertas de seguridad"""
    if 'sesion_activa_id' not in session:
        return jsonify({'success': True, 'alertas': []})
    
    # TODO: Implementar verificación de alertas basada en configuración
    
    return jsonify({
        'success': True,
        'alertas': []
    })


@sesion_bp.route('/sesion/historial', methods=['GET'])
def obtener_historial_sesiones():
    """Obtiene el historial de sesiones del paciente"""
    if not _get_paciente_id():
        return jsonify({'success': False, 'error': 'No autenticado'}), 401
    
    # TODO: Obtener de BD
    
    return jsonify({
        'success': True,
        'sesiones': []
    })

