"""
Controlador de Ejercicios - Patrón de Diseño MVC Controller
Responsable de manejar las peticiones HTTP relacionadas con ejercicios
"""
from flask import request, jsonify, session
from typing import Dict, Any
from ..services.ejercicio_service import EjercicioService
from ..services.paciente_service import PacienteService
from ..models.ejercicio import TipoEjercicio


class EjercicioController:
    """Controlador para manejo de ejercicios"""
    
    def __init__(self):
        self.ejercicio_service = EjercicioService()
        self.paciente_service = PacienteService()
    
    def obtener_ejercicios(self) -> Dict[str, Any]:
        """
        Obtiene todos los ejercicios disponibles
        
        Returns:
            Dict con respuesta JSON
        """
        try:
            ejercicios = self.ejercicio_service.obtener_todos_ejercicios()
            return jsonify({
                'success': True,
                'ejercicios': [e.to_dict() for e in ejercicios]
            }), 200
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    def obtener_ejercicios_rehabilitacion(self) -> Dict[str, Any]:
        """
        Obtiene ejercicios de rehabilitación
        
        Returns:
            Dict con respuesta JSON
        """
        try:
            ejercicios = self.ejercicio_service.obtener_ejercicios_rehabilitacion()
            return jsonify({
                'success': True,
                'ejercicios': [e.to_dict() for e in ejercicios]
            }), 200
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    def obtener_ejercicios_terapia_ocupacional(self) -> Dict[str, Any]:
        """
        Obtiene ejercicios de terapia ocupacional
        
        Returns:
            Dict con respuesta JSON
        """
        try:
            ejercicios = self.ejercicio_service.obtener_ejercicios_terapia_ocupacional()
            return jsonify({
                'success': True,
                'ejercicios': [e.to_dict() for e in ejercicios]
            }), 200
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    def obtener_ejercicio_por_id(self, ejercicio_id: str) -> Dict[str, Any]:
        """
        Obtiene un ejercicio específico por ID
        
        Args:
            ejercicio_id: ID del ejercicio
            
        Returns:
            Dict con respuesta JSON
        """
        try:
            ejercicio = self.ejercicio_service.obtener_ejercicio_por_id(ejercicio_id)
            if ejercicio:
                return jsonify({
                    'success': True,
                    'ejercicio': ejercicio.to_dict()
                }), 200
            else:
                return jsonify({'error': 'Ejercicio no encontrado'}), 404
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    def registrar_resultado(self) -> Dict[str, Any]:
        """
        Registra el resultado de un ejercicio
        
        Returns:
            Dict con respuesta JSON
        """
        try:
            # Verificar sesión
            paciente_data = session.get('paciente')
            if not paciente_data:
                return jsonify({'error': 'No hay sesión activa'}), 401
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Datos requeridos'}), 400
            
            ejercicio_id = data.get('ejercicio_id')
            exito = data.get('exito', False)
            tiempo_ejecucion = data.get('tiempo_ejecucion')
            puntuacion = data.get('puntuacion')
            observaciones = data.get('observaciones')
            
            if not ejercicio_id:
                return jsonify({'error': 'ID de ejercicio requerido'}), 400
            
            # Crear objeto paciente
            from ..models.paciente import Paciente
            paciente = Paciente.from_dict(paciente_data)
            
            # Registrar resultado
            resultado = self.ejercicio_service.registrar_resultado(
                paciente, ejercicio_id, exito, tiempo_ejecucion, puntuacion, observaciones
            )
            
            return jsonify({
                'success': True,
                'message': 'Resultado registrado exitosamente',
                'resultado': resultado.to_dict()
            }), 201
            
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    def obtener_historial(self) -> Dict[str, Any]:
        """
        Obtiene el historial de ejercicios del paciente actual
        
        Returns:
            Dict con respuesta JSON
        """
        try:
            # Verificar sesión
            paciente_data = session.get('paciente')
            if not paciente_data:
                return jsonify({'error': 'No hay sesión activa'}), 401
            
            paciente_id = paciente_data.get('id')
            if not paciente_id:
                return jsonify({'error': 'ID de paciente no válido'}), 400
            
            historial = self.paciente_service.obtener_historial_completo(paciente_id)
            
            return jsonify({
                'success': True,
                'historial': [r.to_dict() for r in historial]
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    def obtener_estadisticas_ejercicio(self, ejercicio_id: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas específicas de un ejercicio
        
        Args:
            ejercicio_id: ID del ejercicio
            
        Returns:
            Dict con respuesta JSON
        """
        try:
            # Verificar sesión
            paciente_data = session.get('paciente')
            if not paciente_data:
                return jsonify({'error': 'No hay sesión activa'}), 401
            
            paciente_id = paciente_data.get('id')
            if not paciente_id:
                return jsonify({'error': 'ID de paciente no válido'}), 400
            
            estadisticas = self.ejercicio_service.obtener_estadisticas_ejercicio(
                paciente_id, ejercicio_id
            )
            
            return jsonify({
                'success': True,
                'estadisticas': estadisticas
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    def obtener_recomendacion(self) -> Dict[str, Any]:
        """
        Obtiene una recomendación de ejercicio para el paciente
        
        Returns:
            Dict con respuesta JSON
        """
        try:
            # Verificar sesión
            paciente_data = session.get('paciente')
            if not paciente_data:
                return jsonify({'error': 'No hay sesión activa'}), 401
            
            paciente_id = paciente_data.get('id')
            if not paciente_id:
                return jsonify({'error': 'ID de paciente no válido'}), 400
            
            recomendacion = self.ejercicio_service.obtener_recomendacion_ejercicio(paciente_id)
            
            if recomendacion:
                return jsonify({
                    'success': True,
                    'recomendacion': recomendacion.to_dict()
                }), 200
            else:
                return jsonify({
                    'success': True,
                    'recomendacion': None,
                    'message': 'No hay recomendaciones disponibles'
                }), 200
            
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
