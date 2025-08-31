"""
Configuración del Backend - Patrón de Diseño Configuration
Responsable de manejar la configuración de la aplicación
"""
import os
from typing import Dict, Any


class Config:
    """Clase base de configuración"""
    
    # Configuración básica
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'rehavr_secret_key_2024'
    DEBUG = False
    TESTING = False
    
    # Configuración de la base de datos
    DATA_PATH = os.environ.get('DATA_PATH') or 'data/pacientes'
    HISTORIAL_PATH = os.environ.get('HISTORIAL_PATH') or 'data/pacientes/historial'
    
    # Configuración de MySQL
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or '127.0.0.1'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'overload'
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'rehabilitacion_virtual'
    MYSQL_CHARSET = os.environ.get('MYSQL_CHARSET') or 'utf8mb4'
    
    # Configuración de CORS
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
    
    # Configuración de sesiones
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
    
    # Configuración de logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @staticmethod
    def init_app(app):
        """Inicializa la aplicación con la configuración"""
        pass


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    
    # Configuración adicional para desarrollo
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:5000']


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    # Configuración de seguridad para producción
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'rehavr_secret_key_2024'


class TestingConfig(Config):
    """Configuración para pruebas"""
    TESTING = True
    DEBUG = True
    
    # Configuración específica para pruebas
    DATA_PATH = 'tests/data/pacientes'
    HISTORIAL_PATH = 'tests/data/pacientes/historial'
    MYSQL_DATABASE = 'rehabilitacion_test'


# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: str = None) -> Config:
    """
    Obtiene la configuración según el entorno
    
    Args:
        config_name: Nombre de la configuración
        
    Returns:
        Config: Objeto de configuración
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])


def get_database_config() -> Dict[str, Any]:
    """
    Obtiene la configuración de la base de datos
    
    Returns:
        Dict: Configuración de la base de datos
    """
    return {
        'data_path': os.environ.get('DATA_PATH', 'data/pacientes'),
        'historial_path': os.environ.get('HISTORIAL_PATH', 'data/pacientes/historial'),
        'backup_enabled': os.environ.get('BACKUP_ENABLED', 'false').lower() == 'true',
        'backup_interval': int(os.environ.get('BACKUP_INTERVAL', 24)),  # horas
        'mysql_host': os.environ.get('MYSQL_HOST', '127.0.0.1'),
        'mysql_port': int(os.environ.get('MYSQL_PORT', 3306)),
        'mysql_user': os.environ.get('MYSQL_USER', 'root'),
        'mysql_password': os.environ.get('MYSQL_PASSWORD', 'overload'),
        'mysql_database': os.environ.get('MYSQL_DATABASE', 'rehabilitacion_virtual'),
        'mysql_charset': os.environ.get('MYSQL_CHARSET', 'utf8mb4')
    }


def get_mysql_config() -> Dict[str, Any]:
    """
    Obtiene la configuración específica de MySQL
    
    Returns:
        Dict: Configuración de MySQL
    """
    return {
        'host': os.environ.get('MYSQL_HOST', '127.0.0.1'),
        'port': int(os.environ.get('MYSQL_PORT', 3306)),
        'user': os.environ.get('MYSQL_USER', 'root'),
        'password': os.environ.get('MYSQL_PASSWORD', 'overload'),
        'database': os.environ.get('MYSQL_DATABASE', 'rehabilitacion_virtual'),
        'charset': os.environ.get('MYSQL_CHARSET', 'utf8mb4'),
        'autocommit': True,
        'pool_size': int(os.environ.get('MYSQL_POOL_SIZE', 5)),
        'pool_recycle': int(os.environ.get('MYSQL_POOL_RECYCLE', 3600))
    }


def get_security_config() -> Dict[str, Any]:
    """
    Obtiene la configuración de seguridad
    
    Returns:
        Dict: Configuración de seguridad
    """
    return {
        'secret_key': os.environ.get('SECRET_KEY', 'rehavr_secret_key_2024'),
        'session_lifetime': int(os.environ.get('SESSION_LIFETIME', 3600)),
        'max_login_attempts': int(os.environ.get('MAX_LOGIN_ATTEMPTS', 5)),
        'lockout_duration': int(os.environ.get('LOCKOUT_DURATION', 300)),  # 5 minutos
        'password_min_length': int(os.environ.get('PASSWORD_MIN_LENGTH', 6))
    }


def get_cors_config() -> Dict[str, Any]:
    """
    Obtiene la configuración de CORS
    
    Returns:
        Dict: Configuración de CORS
    """
    origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000')
    return {
        'origins': [origin.strip() for origin in origins.split(',')],
        'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        'allow_headers': ['Content-Type', 'Authorization'],
        'supports_credentials': True
    }
