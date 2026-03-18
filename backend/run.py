"""
Archivo Principal del Backend - Entry Point
Responsable de iniciar la aplicación Flask
"""
import os
import sys

# Agregar el directorio raíz al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Crear la aplicación
app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Configuración del servidor
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Iniciando RehaVR Backend...")
    print(f"Servidor: http://{host}:{port}")
    print(f"Modo debug: {debug}")
    print(f"Entorno: {os.environ.get('FLASK_ENV', 'development')}")
    print("=" * 50)
    
    # Ejecutar la aplicación
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )
