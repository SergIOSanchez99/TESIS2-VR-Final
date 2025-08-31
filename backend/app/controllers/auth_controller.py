"""
Controlador de Autenticación - Patrón de Diseño MVC Controller
Responsable de manejar las peticiones HTTP relacionadas con autenticación
"""
from flask import request, jsonify, session
from typing import Dict, Any
from ..services.paciente_service import PacienteService


class AuthController:
    """Controlador para manejo de autenticación de pacientes"""
    
    def __init__(self):
        self.paciente_service = PacienteService()
    
    def registrar_paciente(self) -> Dict[str, Any]:
        """
        Registra un nuevo paciente
        
        Returns:
            Dict con respuesta JSON
        """
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Datos requeridos'}), 400
            
            nombre = data.get('nombre', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            edad = data.get('edad', '').strip()
            
            # Validar datos requeridos
            if not nombre or not email or not password or not edad:
                return jsonify({'error': 'Todos los campos son requeridos'}), 400
            
            # Intentar registrar
            exito, mensaje, paciente = self.paciente_service.registrar_paciente(nombre, email, password, edad)
            
            if exito:
                # Establecer sesión (sin contraseña)
                session['paciente'] = paciente.to_dict_safe()
                return jsonify({
                    'success': True,
                    'message': mensaje,
                    'paciente': paciente.to_dict_safe()
                }), 201
            else:
                return jsonify({'error': mensaje}), 400
                
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    def iniciar_sesion(self) -> Dict[str, Any]:
        """
        Inicia sesión de un paciente
        
        Returns:
            Dict con respuesta JSON
        """
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Datos requeridos'}), 400
            
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            
            # Validar datos requeridos
            if not email or not password:
                return jsonify({'error': 'Correo electrónico y contraseña son requeridos'}), 400
            
            # Intentar autenticar
            exito, mensaje, paciente = self.paciente_service.autenticar_paciente(email, password)
            
            if exito:
                # Establecer sesión (sin contraseña)
                session['paciente'] = paciente.to_dict_safe()
                return jsonify({
                    'success': True,
                    'message': mensaje,
                    'paciente': paciente.to_dict_safe()
                }), 200
            else:
                return jsonify({'error': mensaje}), 401
                
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    def cerrar_sesion(self) -> Dict[str, Any]:
        """
        Cierra la sesión del paciente
        
        Returns:
            Dict con respuesta JSON
        """
        try:
            session.pop('paciente', None)
            return jsonify({
                'success': True,
                'message': 'Sesión cerrada exitosamente'
            }), 200
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    def obtener_paciente_actual(self) -> Dict[str, Any]:
        """
        Obtiene información del paciente actual
        
        Returns:
            Dict con respuesta JSON
        """
        try:
            paciente_data = session.get('paciente')
            if not paciente_data:
                return jsonify({'error': 'No hay sesión activa'}), 401
            
            paciente_id = paciente_data.get('id')
            if not paciente_id:
                return jsonify({'error': 'ID de paciente no válido'}), 400
            
            # Obtener estadísticas completas
            estadisticas = self.paciente_service.obtener_estadisticas_paciente(paciente_id)
            
            return jsonify({
                'success': True,
                'paciente': estadisticas
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    def verificar_sesion(self) -> Dict[str, Any]:
        """
        Verifica si hay una sesión activa
        
        Returns:
            Dict con respuesta JSON
        """
        try:
            paciente_data = session.get('paciente')
            if paciente_data:
                return jsonify({
                    'success': True,
                    'autenticado': True,
                    'paciente': paciente_data
                }), 200
            else:
                return jsonify({
                    'success': True,
                    'autenticado': False
                }), 200
                
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
