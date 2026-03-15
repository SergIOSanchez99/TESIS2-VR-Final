"""
Controlador de Configuración - Endpoints para gestión de configuraciones
"""
from flask import Blueprint, request, jsonify, session
from app.services.configuracion_service import ConfiguracionService
from app.models.configuracion import ConfiguracionPaciente

configuracion_bp = Blueprint('configuracion', __name__)
config_service = ConfiguracionService()


def _get_paciente_id():
    """Obtiene el ID del paciente de la sesión activa. Retorna None si no hay sesión."""
    paciente_data = session.get('paciente')
    if not paciente_data:
        return None
    return paciente_data.get('id')


@configuracion_bp.route('/configuracion', methods=['GET'])
def obtener_configuracion():
    """Obtiene la configuración del paciente actual"""
    paciente_id = _get_paciente_id()
    if not paciente_id:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401

    config = config_service.crear_configuracion_default(paciente_id)

    return jsonify({
        'success': True,
        'configuracion': config.to_dict()
    })


@configuracion_bp.route('/configuracion/calibracion', methods=['PUT'])
def actualizar_calibracion():
    """Actualiza la calibración física del paciente"""
    paciente_id = _get_paciente_id()
    if not paciente_id:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Cuerpo de la solicitud requerido (JSON)'}), 400
    config = config_service.crear_configuracion_default(paciente_id)

    resultado = config_service.actualizar_calibracion(
        config,
        altura_cm=data.get('altura_cm'),
        rango_hombro=data.get('rango_hombro'),
        rango_codo=data.get('rango_codo'),
        rango_muneca=data.get('rango_muneca')
    )

    if not resultado.get('valido'):
        return jsonify({'success': False, **resultado}), 400

    return jsonify({'success': True, **resultado})


@configuracion_bp.route('/configuracion/accesibilidad', methods=['PUT'])
def actualizar_accesibilidad():
    """Actualiza la configuración de accesibilidad"""
    paciente_id = _get_paciente_id()
    if not paciente_id:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Cuerpo de la solicitud requerido (JSON)'}), 400
    config = config_service.crear_configuracion_default(paciente_id)

    resultado = config_service.actualizar_accesibilidad(
        config,
        modo=data.get('modo'),
        manos=data.get('manos'),
        velocidad=data.get('velocidad'),
        tamano=data.get('tamano'),
        dificultad_adaptativa=data.get('dificultad_adaptativa'),
        controles_simplificados=data.get('controles_simplificados'),
        texto_grande=data.get('texto_grande'),
        alto_contraste=data.get('alto_contraste')
    )

    if not resultado.get('valido'):
        return jsonify({'success': False, **resultado}), 400

    return jsonify({'success': True, **resultado})


@configuracion_bp.route('/configuracion/seguridad', methods=['PUT'])
def actualizar_seguridad():
    """Actualiza la configuración de seguridad"""
    paciente_id = _get_paciente_id()
    if not paciente_id:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Cuerpo de la solicitud requerido (JSON)'}), 400
    config = config_service.crear_configuracion_default(paciente_id)

    resultado = config_service.actualizar_seguridad(
        config,
        limite_tiempo=data.get('limite_tiempo'),
        intervalo_descanso=data.get('intervalo_descanso'),
        duracion_descanso=data.get('duracion_descanso'),
        alerta_movimientos=data.get('alerta_movimientos'),
        pausa_auto=data.get('pausa_auto'),
        tiempo_inactividad=data.get('tiempo_inactividad'),
        zona_delimitada=data.get('zona_delimitada'),
        antimareo=data.get('antimareo')
    )

    if not resultado.get('valido'):
        return jsonify({'success': False, **resultado}), 400

    return jsonify({'success': True, **resultado})


@configuracion_bp.route('/configuracion/preset/<preset>', methods=['POST'])
def aplicar_preset(preset):
    """Aplica un preset de configuración"""
    paciente_id = _get_paciente_id()
    if not paciente_id:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401

    config = config_service.crear_configuracion_default(paciente_id)
    resultado = config_service.aplicar_preset_accesibilidad(config, preset)

    if not resultado.get('valido'):
        return jsonify({'success': False, **resultado}), 400

    return jsonify({'success': True, **resultado})


@configuracion_bp.route('/configuracion/recomendaciones', methods=['GET'])
def obtener_recomendaciones():
    """Obtiene recomendaciones personalizadas"""
    paciente_id = _get_paciente_id()
    if not paciente_id:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401

    config = config_service.crear_configuracion_default(paciente_id)
    recomendaciones = config_service.obtener_recomendaciones(config)

    return jsonify({'success': True, **recomendaciones})

