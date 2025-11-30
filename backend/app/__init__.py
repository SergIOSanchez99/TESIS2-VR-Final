"""
Aplicación Flask Principal - Factory Pattern
Responsable de crear y configurar la aplicación Flask
"""
from flask import Flask
from flask_cors import CORS
from flask_session import Session
import logging
from logging.handlers import RotatingFileHandler
import os

from .controllers.auth_controller import AuthController
from .controllers.ejercicio_controller import EjercicioController


def create_app(config_name='development'):
    """
    Factory function para crear la aplicación Flask
    
    Args:
        config_name: Nombre de la configuración a usar
        
    Returns:
        Flask: Aplicación Flask configurada
    """
    # Importar configuración
    from config.settings import get_config, get_cors_config
    
    # Crear aplicación con template_folder personalizado
    template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'frontend', 'src', 'templates')
    static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'frontend', 'src', 'assets', 'static')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    
    # Configurar aplicación
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Inicializar extensiones
    init_extensions(app)
    
    # Configurar logging
    setup_logging(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Configurar manejo de errores
    register_error_handlers(app)
    
    return app


def init_extensions(app):
    """Inicializa las extensiones de Flask"""
    # Configurar CORS
    from config.settings import get_cors_config
    cors_config = get_cors_config()
    CORS(app, **cors_config)
    
    # Crear directorio de sesiones si no existe
    session_dir = app.config.get('SESSION_FILE_DIR')
    if session_dir and not os.path.exists(session_dir):
        os.makedirs(session_dir, exist_ok=True)
    
    # Configurar sesiones
    Session(app)


def setup_logging(app):
    """Configura el sistema de logging"""
    if not app.debug and not app.testing:
        # Crear directorio de logs si no existe
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Configurar archivo de log
        file_handler = RotatingFileHandler(
            'logs/rehavr.log', 
            maxBytes=10240000, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('RehaVR startup')


def register_blueprints(app):
    """Registra los blueprints de la aplicación"""
    from .routes import auth_bp, ejercicio_bp, main_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(ejercicio_bp, url_prefix='/api/ejercicios')


def register_error_handlers(app):
    """Registra los manejadores de errores"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Recurso no encontrado'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Error interno del servidor'}, 500
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return {'error': 'Solicitud incorrecta'}, 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        return {'error': 'No autorizado'}, 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return {'error': 'Acceso prohibido'}, 403
